"""Sensor entities for Plantmark plants."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import UnitOfTime, UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from . import PlantmarkConfigEntry
from .entity import PlantmarkEntity


@dataclass(frozen=True, kw_only=True)
class PlantmarkSensorDescription(SensorEntityDescription):
    """Describe how to read a Plantmark sensor value."""

    value_fn: Callable[[dict[str, Any]], Any]


SENSORS: tuple[PlantmarkSensorDescription, ...] = (
    PlantmarkSensorDescription(
        key="next_watering",
        translation_key="next_watering",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:calendar-clock",
        value_fn=lambda plant: _as_datetime(plant.get("next_watering")),
    ),
    PlantmarkSensorDescription(
        key="last_watered",
        translation_key="last_watered",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:watering-can",
        value_fn=lambda plant: _as_datetime(plant.get("last_watered")),
    ),
    PlantmarkSensorDescription(
        key="watering_interval",
        translation_key="watering_interval",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        icon="mdi:calendar-sync",
        value_fn=lambda plant: _active_watering_interval(plant),
    ),
    PlantmarkSensorDescription(
        key="last_watering_amount",
        translation_key="last_watering_amount",
        device_class=SensorDeviceClass.VOLUME,
        native_unit_of_measurement=UnitOfVolume.MILLILITERS,
        icon="mdi:cup-water",
        value_fn=lambda plant: plant.get("last_watering_amount_ml"),
    ),
    PlantmarkSensorDescription(
        key="days_until_watering",
        translation_key="days_until_watering",
        native_unit_of_measurement=UnitOfTime.DAYS,
        icon="mdi:calendar-today",
        value_fn=lambda plant: _days_until(plant.get("next_watering")),
    ),
    PlantmarkSensorDescription(
        key="season",
        translation_key="season",
        device_class=SensorDeviceClass.ENUM,
        options=["summer", "winter"],
        icon="mdi:theme-light-dark",
        value_fn=lambda plant: plant.get("current_season"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PlantmarkConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors and add entities for plants discovered later."""
    coordinator = entry.runtime_data
    known: set[str] = set()

    def _add_new_plants() -> None:
        new_ids = set(coordinator.data) - known
        if not new_ids:
            return
        async_add_entities(
            PlantmarkSensor(coordinator, plant_id, description)
            for plant_id in sorted(new_ids)
            for description in SENSORS
        )
        known.update(new_ids)

    _add_new_plants()
    entry.async_on_unload(coordinator.async_add_listener(_add_new_plants))


class PlantmarkSensor(PlantmarkEntity, SensorEntity):
    """A sensor backed by one field or calculation from a plant."""

    entity_description: PlantmarkSensorDescription

    def __init__(self, coordinator, plant_id, description) -> None:
        super().__init__(coordinator, plant_id, description.key)
        self.entity_description = description

    @property
    def native_value(self):
        """Return the sensor's current value."""
        return self.entity_description.value_fn(self.plant or {})


def _as_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    parsed = dt_util.parse_datetime(value)
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt_util.UTC)
    return parsed


def _days_until(value: Any) -> int | None:
    parsed = _as_datetime(value)
    if parsed is None:
        return None
    return (dt_util.as_local(parsed).date() - dt_util.now().date()).days


def _active_watering_interval(plant: dict[str, Any]) -> int | None:
    season = plant.get("current_season")
    if season == "summer" and plant.get("watering_interval_summer") is not None:
        value = plant["watering_interval_summer"]
        return value if isinstance(value, int) else None
    if season == "winter" and plant.get("watering_interval_winter") is not None:
        value = plant["watering_interval_winter"]
        return value if isinstance(value, int) else None
    value = plant.get("watering_interval_days")
    return value if isinstance(value, int) else None

