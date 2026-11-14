"""Constants for the Plantmark integration."""

from __future__ import annotations

from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "plantmark"

CONF_LIBRARY_NAME: Final = "library_name"
CONF_PLANTS: Final = "plants"
CONF_DEFAULT_WATER_AMOUNT: Final = "default_water_amount_ml"

DEFAULT_LIBRARY_NAME: Final = "Plantmark"
DEFAULT_WATERING_INTERVAL: Final = 7
DEFAULT_WATER_AMOUNT: Final = 0

PLATFORMS: Final = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CALENDAR,
]

