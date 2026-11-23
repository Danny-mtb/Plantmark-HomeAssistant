"""In-memory coordinator backed by the Home Assistant config entry."""

from __future__ import annotations

import logging
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import CONF_PLANTS, DOMAIN
from .plant import (
    global_reminder_settings,
    season_for_month,
    watering_interval_range,
)

_LOGGER = logging.getLogger(__name__)


class PlantmarkDataUpdateCoordinator(DataUpdateCoordinator[dict[str, dict[str, Any]]]):
    """Keep Plantmark entities synchronized with config-entry storage."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.calendar_sync: Any = None
        super().__init__(
            hass,
            logger=_LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=timedelta(minutes=15),
        )

    async def _async_update_data(self) -> dict[str, dict[str, Any]]:
        """Refresh calculated values from local config-entry storage."""
        plants = deepcopy(list(self.entry.options.get(CONF_PLANTS, [])))
        changed = self._adjust_watering_for_moisture(plants)
        if await self._async_send_watering_reminders(plants):
            changed = True
        if changed:
            self._save_plants(plants)
        return self._plants_from_list(plants)

    async def async_water_plant(
        self, plant_id: str, *, amount_ml: int | None = None
    ) -> None:
        """Record watering and persist the next due date in Home Assistant."""
        plants = deepcopy(list(self.entry.options.get(CONF_PLANTS, [])))
        now = dt_util.now()

        for plant in plants:
            if str(plant.get("id")) != plant_id:
                continue
            minimum, maximum = watering_interval_range(
                plant, season_for_month(now.month)
            )
            plant["last_watered"] = now.isoformat()
            plant["next_watering"] = (now + timedelta(days=minimum)).isoformat()
            plant["next_watering_end"] = (now + timedelta(days=maximum)).isoformat()
            plant["last_notification_for"] = None
            plant["last_moisture_adjustment"] = None
            if amount_ml is not None and amount_ml > 0:
                plant["last_watering_amount_ml"] = amount_ml
            break
        else:
            raise ValueError(f"Unknown plant: {plant_id}")

        self._save_plants(plants)
        self.async_set_updated_data(self._plants_from_list(plants))
        try:
            await self.hass.services.async_call(
                "persistent_notification",
                "dismiss",
                {"notification_id": f"plantmark_{plant_id}"},
                blocking=False,
            )
        except HomeAssistantError as err:
            _LOGGER.debug(
                "Could not dismiss watering reminder for %s: %s", plant_id, err
            )

    def async_replace_plants(self, plants: list[dict[str, Any]]) -> None:
        """Immediately expose plants changed through the Plantmark panel."""
        self.async_set_updated_data(self._plants_from_list(plants))

    def _plants_from_options(self) -> dict[str, dict[str, Any]]:
        return self._plants_from_list(self.entry.options.get(CONF_PLANTS, []))

    def _plants_from_list(self, plants: Any) -> dict[str, dict[str, Any]]:
        if not isinstance(plants, list):
            return {}
        season = season_for_month(dt_util.now().month)
        result: dict[str, dict[str, Any]] = {}
        for plant in plants:
            if (
                not isinstance(plant, dict)
                or not plant.get("id")
                or not plant.get("name")
            ):
                continue
            current = dict(plant)
            current["current_season"] = season
            result[str(plant["id"])] = current
        return result

    def _adjust_watering_for_moisture(self, plants: list[dict[str, Any]]) -> bool:
        """Postpone due watering windows while the configured soil is moist."""
        now = dt_util.now()
        today = dt_util.as_local(now).date().isoformat()
        changed = False
        for plant in plants:
            if not plant.get("moisture_control_enabled"):
                continue
            sensor_id = str(plant.get("water_sensor_entity_id") or "")
            state = self.hass.states.get(sensor_id)
            start = _as_datetime(plant.get("next_watering"))
            if state is None or start is None or now < start:
                continue
            try:
                moisture = float(state.state)
                threshold = float(plant.get("moisture_threshold_percent", 35))
            except (TypeError, ValueError):
                continue
            if moisture < threshold or plant.get("last_moisture_adjustment") == today:
                continue
            end = _as_datetime(plant.get("next_watering_end")) or start
            delay = plant.get("moisture_delay_days", 1)
            delay = delay if isinstance(delay, int) and 1 <= delay <= 30 else 1
            window_width = max(timedelta(0), end - start)
            shifted_start = max(
                start + timedelta(days=delay), now + timedelta(days=delay)
            )
            plant["next_watering"] = shifted_start.isoformat()
            plant["next_watering_end"] = (shifted_start + window_width).isoformat()
            plant["last_moisture_adjustment"] = today
            plant["last_notification_for"] = None
            changed = True
        return changed

    async def _async_send_watering_reminders(
        self, plants: list[dict[str, Any]]
    ) -> bool:
        """Send each due reminder to the central Plantmark target once."""
        enabled, target = global_reminder_settings(dict(self.entry.options))
        if not enabled or not target:
            return False
        now = dt_util.now()
        changed = False
        for plant in plants:
            start = _as_datetime(plant.get("next_watering"))
            if start is None or now < start:
                continue
            marker = start.isoformat()
            if plant.get("last_notification_for") == marker:
                continue
            try:
                await self._async_send_notification(plant, target)
            except HomeAssistantError as err:
                _LOGGER.warning(
                    "Could not send watering reminder for %s: %s",
                    plant.get("name"),
                    err,
                )
                continue
            plant["last_notification_for"] = marker
            changed = True
        return changed

    async def _async_send_notification(
        self, plant: dict[str, Any], target: str
    ) -> None:
        title, message = self._notification_text(plant)
        data = {"title": title, "message": message}
        if target == "persistent_notification":
            data["notification_id"] = f"plantmark_{plant.get('id')}"
            await self.hass.services.async_call(
                "persistent_notification", "create", data, blocking=False
            )
            return
        if target.startswith("entity:notify."):
            await self.hass.services.async_call(
                "notify",
                "send_message",
                data,
                blocking=False,
                target={"entity_id": target.removeprefix("entity:")},
            )
            return
        if target.startswith("service:notify."):
            await self.hass.services.async_call(
                "notify",
                target.removeprefix("service:notify."),
                data,
                blocking=False,
            )
            return
        raise HomeAssistantError("Unsupported Plantmark notification target")

    def _notification_text(self, plant: dict[str, Any]) -> tuple[str, str]:
        name = str(plant.get("name") or "Plant")
        end = _as_datetime(plant.get("next_watering_end"))
        language = str(self.hass.config.language or "en").lower()
        if language.startswith("de"):
            title = f"{name} gießen"
            message = f"Der Gießzeitraum für {name} hat begonnen."
            if end is not None:
                message += f" Empfohlen bis {dt_util.as_local(end):%d.%m.%Y}."
            return title, message
        title = f"Water {name}"
        message = f"The watering window for {name} has started."
        if end is not None:
            message += f" Recommended by {dt_util.as_local(end):%Y-%m-%d}."
        return title, message

    def _save_plants(self, plants: list[dict[str, Any]]) -> None:
        options = dict(self.entry.options)
        options[CONF_PLANTS] = plants
        self.hass.config_entries.async_update_entry(self.entry, options=options)


def _as_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    parsed = dt_util.parse_datetime(value)
    if parsed is not None and parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt_util.UTC)
    return parsed
