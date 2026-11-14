"""Entity helpers shared by Plantmark platforms."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PlantmarkDataUpdateCoordinator


class PlantmarkEntity(CoordinatorEntity[PlantmarkDataUpdateCoordinator]):
    """Base class for entities belonging to a Plantmark plant."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PlantmarkDataUpdateCoordinator,
        plant_id: str,
        entity_key: str,
    ) -> None:
        super().__init__(coordinator)
        self.plant_id = plant_id
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{plant_id}_{entity_key}"

    @property
    def plant(self) -> dict[str, Any] | None:
        """Return the latest stored data for this plant."""
        return self.coordinator.data.get(self.plant_id)

    @property
    def available(self) -> bool:
        """Mark deleted plants unavailable until the entry reload completes."""
        return super().available and self.plant is not None

    @property
    def entity_picture(self) -> str | None:
        """Use the configured plant image on entity cards when available."""
        image_url = (self.plant or {}).get("image_url")
        return image_url if isinstance(image_url, str) and image_url else None

    @property
    def device_info(self) -> DeviceInfo:
        """Represent every plant as a Home Assistant device."""
        plant = self.plant or {}
        model = plant.get("scientific_name") or "Plant"
        return DeviceInfo(
            identifiers={
                (DOMAIN, f"{self.coordinator.entry.entry_id}_{self.plant_id}")
            },
            manufacturer="Plantmark",
            model=str(model),
            name=str(plant.get("name") or self.plant_id),
        )

