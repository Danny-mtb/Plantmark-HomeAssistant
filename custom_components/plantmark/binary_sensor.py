"""Binary warning sensors for Plantmark."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from . import PlantmarkConfigEntry
from .entity import PlantmarkEntity


@dataclass(frozen=True, kw_only=True)
class PlantmarkBinarySensorDescription(BinarySensorEntityDescription):
    """Describe a Plantmark warning sensor."""

    value_fn: Callable[[dict[str, Any]], bool]


BINARY_SENSORS = (
    PlantmarkBinarySensorDescription(
        key="needs_water",
        translation_key="needs_water",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:water-alert",
        value_fn=lambda plant: _is_due(plant.get("next_watering")),
    ),
    PlantmarkBinarySensorDescription(
        key="toxic_to_cats",
        translation_key="toxic_to_cats",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:cat",
        value_fn=lambda plant: bool(plant.get("is_toxic_to_cats")),
    ),
    PlantmarkBinarySensorDescription(
        key="toxic_to_dogs",
        translation_key="toxic_to_dogs",
        device_class=BinarySensorDeviceClass.PROBLEM,
        icon="mdi:dog",
        value_fn=lambda plant: bool(plant.get("is_toxic_to_dogs")),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PlantmarkConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data
    entities: dict[str, list[PlantmarkBinarySensor]] = {}

    def _sync_plants() -> None:
        current_ids = set(coordinator.data)
        for plant_id in set(entities) - current_ids:
            for entity in entities.pop(plant_id):
                hass.async_create_task(
                    entity.async_remove(),
                    f"Remove Plantmark binary sensor {entity.entity_id}",
                )

        new_entities = [
            PlantmarkBinarySensor(coordinator, plant_id, description)
            for plant_id in sorted(current_ids - set(entities))
            for description in BINARY_SENSORS
        ]
        for entity in new_entities:
            entities.setdefault(entity.plant_id, []).append(entity)
        if new_entities:
            async_add_entities(new_entities)

    _sync_plants()
    entry.async_on_unload(coordinator.async_add_listener(_sync_plants))


class PlantmarkBinarySensor(PlantmarkEntity, BinarySensorEntity):
    """A warning flag for a Plantmark plant."""

    entity_description: PlantmarkBinarySensorDescription

    def __init__(self, coordinator, plant_id, description) -> None:
        super().__init__(coordinator, plant_id, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool:
        return self.entity_description.value_fn(self.plant or {})


def _is_due(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = dt_util.parse_datetime(value)
    if parsed is None:
        return False
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt_util.UTC)
    return parsed <= dt_util.now()

