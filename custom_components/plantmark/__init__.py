"""Plantmark integration for Home Assistant."""

from __future__ import annotations

from typing import TypeAlias

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .calendar_sync import PlantmarkCalendarSync
from .const import PLATFORMS
from .coordinator import PlantmarkDataUpdateCoordinator
from .panel import async_remove_panel, async_setup_panel, async_sync_devices

PlantmarkConfigEntry: TypeAlias = ConfigEntry[PlantmarkDataUpdateCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: PlantmarkConfigEntry) -> bool:
    """Set up a native Plantmark library from a config entry."""
    coordinator = PlantmarkDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await async_setup_panel(hass)
    async_sync_devices(hass, entry)
    calendar_sync = PlantmarkCalendarSync(hass, entry)
    coordinator.calendar_sync = calendar_sync
    entry.async_on_unload(coordinator.async_add_listener(calendar_sync.async_schedule))
    entry.async_on_unload(calendar_sync.async_shutdown)
    calendar_sync.async_schedule()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: PlantmarkConfigEntry) -> bool:
    """Unload a Plantmark config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        async_remove_panel(hass)
    return unloaded

