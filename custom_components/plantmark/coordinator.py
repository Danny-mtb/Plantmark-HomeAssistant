"""In-memory coordinator backed by the Home Assistant config entry."""

from __future__ import annotations

import logging
from copy import deepcopy
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import CONF_PLANTS, DOMAIN

_LOGGER = logging.getLogger(__name__)


class PlantmarkDataUpdateCoordinator(DataUpdateCoordinator[dict[str, dict[str, Any]]]):
    """Keep Plantmark entities synchronized with config-entry storage."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        super().__init__(
            hass,
            logger=_LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=timedelta(minutes=15),
        )

    async def _async_update_data(self) -> dict[str, dict[str, Any]]:
        """Refresh calculated values from local config-entry storage."""
        return self._plants_from_options()

    async def async_water_plant(
        self, plant_id: str, *, amount_ml: int | None = None
    ) -> None:
        """Record watering and persist the next due date in Home Assistant."""
        plants = deepcopy(list(self.entry.options.get(CONF_PLANTS, [])))
        now = dt_util.now()

        for plant in plants:
            if str(plant.get("id")) != plant_id:
                continue
            interval = plant.get("watering_interval_days", 7)
            if not isinstance(interval, int) or interval < 1:
                interval = 7
            plant["last_watered"] = now.isoformat()
            plant["next_watering"] = (now + timedelta(days=interval)).isoformat()
            if amount_ml is not None and amount_ml > 0:
                plant["last_watering_amount_ml"] = amount_ml
            break
        else:
            raise ValueError(f"Unknown plant: {plant_id}")

        options = dict(self.entry.options)
        options[CONF_PLANTS] = plants
        self.hass.config_entries.async_update_entry(self.entry, options=options)
        self.async_set_updated_data(self._plants_from_list(plants))

    def async_replace_plants(self, plants: list[dict[str, Any]]) -> None:
        """Immediately expose plants changed through the Plantmark panel."""
        self.async_set_updated_data(self._plants_from_list(plants))

    def _plants_from_options(self) -> dict[str, dict[str, Any]]:
        return self._plants_from_list(self.entry.options.get(CONF_PLANTS, []))

    @staticmethod
    def _plants_from_list(plants: Any) -> dict[str, dict[str, Any]]:
        if not isinstance(plants, list):
            return {}
        season = "summer" if 4 <= dt_util.now().month <= 9 else "winter"
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

