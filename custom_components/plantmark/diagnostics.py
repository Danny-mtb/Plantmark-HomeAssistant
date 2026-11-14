"""Privacy-aware diagnostics for Plantmark."""

from __future__ import annotations

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import PlantmarkConfigEntry

TO_REDACT = {
    "area_id",
    "image_url",
    "location",
    "notes",
    "apartment_name",
    "room_name",
    "water_sensor_entity_id",
}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: PlantmarkConfigEntry
) -> dict:
    """Return data useful for issue reports without leaking credentials."""
    coordinator = entry.runtime_data
    return async_redact_data(
        {
            "config_entry": entry.as_dict(),
            "last_update_success": coordinator.last_update_success,
            "plant_count": len(coordinator.data),
            "plants": list(coordinator.data.values()),
        },
        TO_REDACT,
    )

