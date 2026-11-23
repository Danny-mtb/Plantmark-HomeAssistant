"""Mirror Plantmark watering windows into an existing Home Assistant calendar.

Any calendar entity that supports creating events can be used, for example an
iCloud calendar connected through Home Assistant's CalDAV integration. Plantmark
creates one all-day event per plant and watering window. When the target
calendar also supports deleting events, outdated future Plantmark events are
removed after a plant was watered, postponed or deleted.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import date, datetime, timedelta
from typing import Any

from homeassistant.components.calendar import CalendarEntityFeature, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.debounce import Debouncer
from homeassistant.util import dt as dt_util

from .const import CONF_PLANTS, CONF_SYNC_CALENDAR, DOMAIN

_LOGGER = logging.getLogger(__name__)

MARKER = "Plantmark-ID:"
LOOKBACK = timedelta(days=2)
LOOKAHEAD = timedelta(days=400)


def calendar_targets(hass: HomeAssistant) -> list[dict[str, Any]]:
    """Return writable calendars that Plantmark can synchronize into."""
    registry = er.async_get(hass)
    targets: list[dict[str, Any]] = []
    for state in hass.states.async_all("calendar"):
        entry = registry.async_get(state.entity_id)
        if entry is not None and entry.platform == DOMAIN:
            continue
        features = int(state.attributes.get("supported_features") or 0)
        if not features & CalendarEntityFeature.CREATE_EVENT:
            continue
        targets.append(
            {
                "id": state.entity_id,
                "name": str(state.attributes.get("friendly_name") or state.entity_id),
                "can_delete": bool(features & CalendarEntityFeature.DELETE_EVENT),
            }
        )
    return sorted(targets, key=lambda item: item["name"].casefold())


def desired_events(
    plants: Any, language: str | None
) -> dict[tuple[str, date], dict[str, Any]]:
    """Build the all-day events that should exist for the current plants."""
    german = str(language or "en").lower().startswith("de")
    result: dict[tuple[str, date], dict[str, Any]] = {}
    if not isinstance(plants, list):
        return result
    for plant in plants:
        if not isinstance(plant, dict) or not plant.get("id"):
            continue
        start = _as_datetime(plant.get("next_watering"))
        if start is None:
            continue
        plant_id = str(plant["id"])
        name = str(plant.get("name") or "Plant")
        start_day = dt_util.as_local(start).date()
        end = _as_datetime(plant.get("next_watering_end"))
        end_day = dt_util.as_local(end).date() if end is not None else start_day
        if end_day < start_day:
            end_day = start_day
        summary = f"💧 {name} gießen" if german else f"💧 Water {name}"
        lines = [str(plant.get("scientific_name") or "").strip()]
        location = str(plant.get("location") or "").strip()
        lines.append(f"{MARKER} {plant_id}")
        result[(plant_id, start_day)] = {
            "summary": summary,
            "description": "\n".join(line for line in lines if line),
            "start_date": start_day.isoformat(),
            # Home Assistant expects an exclusive end date for all-day events.
            "end_date": (end_day + timedelta(days=1)).isoformat(),
            **({"location": location} if location else {}),
        }
    return result


def managed_plant_id(event: CalendarEvent) -> str | None:
    """Return the Plantmark plant ID stored in an event description."""
    for line in str(event.description or "").splitlines():
        line = line.strip()
        if line.startswith(MARKER):
            return line.removeprefix(MARKER).strip() or None
    return None


class PlantmarkCalendarSync:
    """Keep one external calendar in step with Plantmark's watering windows."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry
        self._lock = asyncio.Lock()
        # Remote calendars such as iCloud may not list a freshly created event
        # immediately; remember what was created to avoid duplicates.
        self._created: set[tuple[str, str, date]] = set()
        self._debouncer = Debouncer(
            hass,
            _LOGGER,
            cooldown=10,
            immediate=False,
            function=self.async_sync,
        )

    @property
    def target(self) -> str:
        return str(self.entry.options.get(CONF_SYNC_CALENDAR) or "").strip()

    @callback
    def async_schedule(self) -> None:
        """Request a debounced synchronization."""
        if self.target:
            self.hass.async_create_task(self._debouncer.async_call())

    @callback
    def async_shutdown(self) -> None:
        self._debouncer.async_shutdown()

    async def async_sync(self) -> None:
        """Create missing events and remove outdated ones in the target."""
        target = self.target
        if not target:
            return
        async with self._lock:
            try:
                await self._async_sync(target)
            except HomeAssistantError as err:
                _LOGGER.warning("Could not synchronize calendar %s: %s", target, err)

    async def async_clear(self, entity_id: str) -> None:
        """Remove future Plantmark events from a calendar no longer used."""
        async with self._lock:
            entity = self._entity(entity_id)
            if entity is None or not _can_delete(entity):
                return
            try:
                existing = await self._managed_events(entity)
                now = dt_util.now()
                for _, event in existing:
                    if event.end_datetime_local > now:
                        await self._delete(entity, event)
            except HomeAssistantError as err:
                _LOGGER.warning("Could not clean up calendar %s: %s", entity_id, err)
            self._created = {item for item in self._created if item[0] != entity_id}

    async def _async_sync(self, target: str) -> None:
        entity = self._entity(target)
        if entity is None:
            _LOGGER.debug("Calendar %s is not available yet", target)
            return
        desired = desired_events(
            self.entry.options.get(CONF_PLANTS, []), self.hass.config.language
        )
        existing = await self._managed_events(entity)
        present: set[tuple[str, date]] = set()
        now = dt_util.now()
        for plant_id, event in existing:
            key = (plant_id, _event_start(event))
            if key in desired and key not in present:
                present.add(key)
                continue
            # Keep the history of past windows; only tidy up upcoming ones.
            if event.end_datetime_local > now and _can_delete(entity):
                await self._delete(entity, event)

        for key, data in desired.items():
            marker = (target, key[0], key[1])
            if key in present or marker in self._created:
                continue
            await self.hass.services.async_call(
                "calendar",
                "create_event",
                data,
                target={"entity_id": target},
                blocking=True,
            )
            self._created.add(marker)

    async def _managed_events(self, entity: Any) -> list[tuple[str, CalendarEvent]]:
        now = dt_util.now()
        events = await entity.async_get_events(
            self.hass, now - LOOKBACK, now + LOOKAHEAD
        )
        result: list[tuple[str, CalendarEvent]] = []
        for event in events:
            plant_id = managed_plant_id(event)
            if plant_id is not None:
                result.append((plant_id, event))
        return result

    async def _delete(self, entity: Any, event: CalendarEvent) -> None:
        if not event.uid:
            return
        await entity.async_delete_event(
            event.uid, recurrence_id=event.recurrence_id
        )

    def _entity(self, entity_id: str) -> Any:
        component = self.hass.data.get("calendar")
        if component is None:
            return None
        return component.get_entity(entity_id)


def _can_delete(entity: Any) -> bool:
    features = int(getattr(entity, "supported_features", 0) or 0)
    return bool(features & CalendarEntityFeature.DELETE_EVENT)


def _event_start(event: CalendarEvent) -> date:
    start = event.start
    if isinstance(start, datetime):
        return dt_util.as_local(start).date()
    return start


def _as_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    parsed = dt_util.parse_datetime(value)
    if parsed is not None and parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt_util.UTC)
    return parsed
