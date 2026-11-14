"""Plantmark integration for Home Assistant."""

from __future__ import annotations

from typing import TypeAlias

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import PLATFORMS
from .coordinator import PlantmarkDataUpdateCoordinator

PlantmarkConfigEntry: TypeAlias = ConfigEntry[PlantmarkDataUpdateCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: PlantmarkConfigEntry) -> bool:
    """Set up a native Plantmark library from a config entry."""
    coordinator = PlantmarkDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: PlantmarkConfigEntry) -> bool:
    """Unload a Plantmark config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

