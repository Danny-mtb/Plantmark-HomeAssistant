"""Watering buttons for Plantmark."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PlantmarkConfigEntry
from .const import CONF_DEFAULT_WATER_AMOUNT, DEFAULT_WATER_AMOUNT
from .entity import PlantmarkEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PlantmarkConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = entry.runtime_data
    entities: dict[str, PlantmarkWaterButton] = {}

    def _sync_plants() -> None:
        current_ids = set(coordinator.data)
        for plant_id in set(entities) - current_ids:
            entity = entities.pop(plant_id)
            hass.async_create_task(
                entity.async_remove(), f"Remove Plantmark button {entity.entity_id}"
            )

        new_entities = [
            PlantmarkWaterButton(coordinator, plant_id)
            for plant_id in sorted(current_ids - set(entities))
        ]
        entities.update({entity.plant_id: entity for entity in new_entities})
        if new_entities:
            async_add_entities(new_entities)

    _sync_plants()
    entry.async_on_unload(coordinator.async_add_listener(_sync_plants))


class PlantmarkWaterButton(PlantmarkEntity, ButtonEntity):
    """Record watering directly in Home Assistant storage."""

    _attr_translation_key = "water"
    _attr_icon = "mdi:watering-can"

    def __init__(self, coordinator, plant_id) -> None:
        super().__init__(coordinator, plant_id, "water")

    async def async_press(self) -> None:
        amount = self.coordinator.entry.options.get(
            CONF_DEFAULT_WATER_AMOUNT, DEFAULT_WATER_AMOUNT
        )
        try:
            await self.coordinator.async_water_plant(
                self.plant_id,
                amount_ml=amount if isinstance(amount, int) and amount > 0 else None,
            )
        except ValueError as err:
            raise HomeAssistantError(str(err)) from err

