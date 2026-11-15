"""Constants for the Plantmark integration."""

from __future__ import annotations

from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "plantmark"

CONF_LIBRARY_NAME: Final = "library_name"
CONF_PLANTS: Final = "plants"
CONF_DEFAULT_WATER_AMOUNT: Final = "default_water_amount_ml"
CONF_WATERING_REMINDER_ENABLED: Final = "watering_reminder_enabled"
CONF_NOTIFICATION_TARGET: Final = "notification_target"
CONF_PERENUAL_API_KEY: Final = "perenual_api_key"

DEFAULT_LIBRARY_NAME: Final = "Plantmark"
DEFAULT_WATERING_INTERVAL: Final = 7
DEFAULT_WATER_AMOUNT: Final = 0

PLATFORMS: Final = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CALENDAR,
]

