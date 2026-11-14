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
from .plant import watering_interval_range


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
        key="watering_window_end",
        translation_key="watering_window_end",
        device_class=SensorDeviceClass.TIMESTAMP,
        icon="mdi:calendar-end",
        value_fn=lambda plant: _as_datetime(plant.get("next_watering_end")),
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
        key="watering_interval_max",
        translation_key="watering_interval_max",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        icon="mdi:calendar-range",
        value_fn=lambda plant: _active_watering_interval_range(plant)[1],
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
        options=["spring", "summer", "autumn", "winter"],
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
    entities: dict[str, list[PlantmarkSensor]] = {}

    def _sync_plants() -> None:
        current_ids = set(coordinator.data)
        for plant_id in set(entities) - current_ids:
            for entity in entities.pop(plant_id):
                hass.async_create_task(
                    entity.async_remove(), f"Remove Plantmark sensor {entity.entity_id}"
                )

        new_entities = [
            PlantmarkSensor(coordinator, plant_id, description)
            for plant_id in sorted(current_ids - set(entities))
            for description in SENSORS
        ]
        for entity in new_entities:
            entities.setdefault(entity.plant_id, []).append(entity)
        if new_entities:
            async_add_entities(new_entities)

    _sync_plants()
    entry.async_on_unload(coordinator.async_add_listener(_sync_plants))


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

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Expose both ends of an active watering interval."""
        if self.entity_description.key != "watering_interval" or self.plant is None:
            return None
        minimum, maximum = watering_interval_range(
            self.plant, self.plant.get("current_season")
        )
        return {"minimum_days": minimum, "maximum_days": maximum}


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
    return _active_watering_interval_range(plant)[0]


def _active_watering_interval_range(plant: dict[str, Any]) -> tuple[int, int]:
    return watering_interval_range(plant, plant.get("current_season"))
