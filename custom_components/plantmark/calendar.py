"""Upcoming watering calendar for Plantmark."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from . import PlantmarkConfigEntry
from .coordinator import PlantmarkDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PlantmarkConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([PlantmarkWateringCalendar(entry.runtime_data)])


class PlantmarkWateringCalendar(
    CoordinatorEntity[PlantmarkDataUpdateCoordinator], CalendarEntity
):
    """A combined calendar containing the next watering for every plant."""

    _attr_has_entity_name = True
    _attr_translation_key = "watering_calendar"
    _attr_icon = "mdi:calendar-water"

    def __init__(self, coordinator: PlantmarkDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_watering_calendar"

    @property
    def event(self) -> CalendarEvent | None:
        now = dt_util.now()
        upcoming = [event for event in self._events() if event.end >= now]
        return min(upcoming, key=lambda item: item.start, default=None)

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        return [
            event
            for event in self._events()
            if event.start < end_date and event.end > start_date
        ]

    def _events(self) -> list[CalendarEvent]:
        events: list[CalendarEvent] = []
        for plant in self.coordinator.data.values():
            start = _as_datetime(plant.get("next_watering"))
            if start is None:
                continue
            location = plant.get("room_name") or plant.get("location")
            events.append(
                CalendarEvent(
                    start=start,
                    end=start + timedelta(minutes=30),
                    summary=f"Water {plant.get('name', 'plant')}",
                    description=plant.get("scientific_name"),
                    location=location,
                    uid=f"plantmark-{plant.get('id')}-{start.isoformat()}",
                )
            )
        return sorted(events, key=lambda event: event.start)


def _as_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    parsed = dt_util.parse_datetime(value)
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt_util.UTC)
    return parsed

