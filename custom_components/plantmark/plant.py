"""Plant data normalization shared by the config flow and sidebar panel."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from homeassistant.util import dt as dt_util

from .const import (
    CONF_NOTIFICATION_TARGET,
    CONF_PLANTS,
    CONF_WATERING_REMINDER_ENABLED,
    DEFAULT_WATERING_INTERVAL,
)

SEASONS = ("spring", "summer", "autumn", "winter")

_API_TEXT_FIELDS = (
    "api_provider",
    "api_last_synced",
    "perenual_url",
    "common_name",
    "family",
    "plant_type",
    "cycle",
    "watering",
    "watering_guide",
    "sunlight_guide",
    "pruning_guide",
    "watering_interval_source",
    "care_guide_source",
    "watering_quality",
    "watering_period",
    "water_depth_requirement",
    "water_volume_requirement",
    "average_volume_requirement",
    "base_temperature",
    "ph_level",
    "sunlight_duration",
    "temperature_tolerance",
    "spacing_requirement",
    "care_level",
    "description",
    "growth_rate",
    "maintenance",
    "hardiness_min",
    "hardiness_max",
    "flowering_season",
    "fruiting_season",
    "harvest_season",
    "harvest_method",
    "dimensions",
    "pruning_frequency",
    "seeds",
    "image_license_name",
    "image_license_url",
)
_API_LIST_FIELDS = (
    "other_names",
    "origin",
    "sunlight",
    "soil",
    "propagation",
    "attracts",
    "pruning_month",
    "pest_susceptibility",
    "flower_color",
    "fruit_color",
)
_API_BOOL_FIELDS = (
    "indoor",
    "poisonous_to_humans",
    "poisonous_to_pets",
    "watering_interval_estimated",
    "flowers",
    "fruits",
    "edible_fruit",
    "edible_leaf",
    "medicinal",
    "drought_tolerant",
    "salt_tolerant",
    "thorny",
    "invasive",
    "tropical",
    "cones",
    "leaf",
    "rare",
    "cuisine",
)
_PLANT_TEXT_FIELDS = (
    "last_notification_for",
    "last_moisture_adjustment",
)
_PLANT_BOOL_FIELDS = (
    "seasonal_watering_enabled",
    "moisture_control_enabled",
)
_PLANT_INT_FIELDS = (
    "watering_interval_min_days",
    "watering_interval_max_days",
    "moisture_threshold_percent",
    "moisture_delay_days",
)
_WATERING_RANGE_FIELDS = (
    "watering_interval_days",
    "watering_interval_min_days",
    "watering_interval_max_days",
    "seasonal_watering_enabled",
    *(
        f"watering_interval_{season}_{suffix}"
        for season in SEASONS
        for suffix in ("min_days", "max_days")
    ),
)


def new_plant(values: dict[str, Any]) -> dict[str, Any]:
    """Create a normalized plant with its first watering schedule."""
    now = dt_util.now()
    cleaned = _clean_values(values)
    minimum, maximum = watering_interval_range(cleaned, season_for_month(now.month))
    return {
        "id": uuid4().hex,
        **cleaned,
        "last_watered": now.isoformat(),
        "next_watering": (now + timedelta(days=minimum)).isoformat(),
        "next_watering_end": (now + timedelta(days=maximum)).isoformat(),
        "current_season": season_for_month(now.month),
    }


def updated_plant(plant: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    """Apply normalized changes while retaining panel-only legacy data."""
    cleaned = _clean_values(values)
    for panel_field in ("area_id", "water_sensor_entity_id"):
        if panel_field not in values:
            cleaned.pop(panel_field, None)
    updated = {**plant, **cleaned}
    last_watered = dt_util.parse_datetime(str(updated.get("last_watered", "")))
    if last_watered is not None and any(
        field in cleaned and cleaned[field] != plant.get(field)
        for field in _WATERING_RANGE_FIELDS
    ):
        minimum, maximum = watering_interval_range(
            updated, season_for_month(last_watered.month)
        )
        next_watering = (last_watered + timedelta(days=minimum)).isoformat()
        next_watering_end = (last_watered + timedelta(days=maximum)).isoformat()
        schedule_changed = next_watering != plant.get(
            "next_watering"
        ) or next_watering_end != plant.get("next_watering_end")
        updated["next_watering"] = next_watering
        updated["next_watering_end"] = next_watering_end
        if schedule_changed:
            updated["last_notification_for"] = None
            updated["last_moisture_adjustment"] = None
    return updated


def parse_import(raw: str) -> list[dict[str, Any]]:
    """Parse a legacy API response or JSON plant list."""
    payload = json.loads(raw)
    if isinstance(payload, dict):
        payload = payload.get("plants")
    if not isinstance(payload, list):
        raise TypeError("Import must be a list or contain a plants list")

    plants: list[dict[str, Any]] = []
    for source in payload:
        if not isinstance(source, dict) or not str(source.get("name", "")).strip():
            continue
        interval = source.get("watering_interval_days", DEFAULT_WATERING_INTERVAL)
        try:
            interval = max(1, min(365, int(interval)))
        except (TypeError, ValueError):
            interval = DEFAULT_WATERING_INTERVAL
        now = dt_util.now()
        last = _valid_datetime(source.get("last_watered")) or now
        normalized_values = {
            "watering_interval_days": interval,
            **_copy_schedule_values(source),
        }
        minimum, maximum = watering_interval_range(
            normalized_values, season_for_month(last.month)
        )
        next_watering = _valid_datetime(source.get("next_watering")) or (
            last + timedelta(days=minimum)
        )
        next_watering_end = _valid_datetime(source.get("next_watering_end")) or (
            last + timedelta(days=maximum)
        )
        plants.append(
            {
                "id": str(source.get("id") or uuid4().hex),
                "name": str(source["name"]).strip(),
                "scientific_name": _optional_text(source.get("scientific_name")),
                "location": _optional_text(
                    source.get("room_name") or source.get("location")
                ),
                "image_url": _optional_text(source.get("image_url")),
                "area_id": _optional_text(source.get("area_id")),
                "water_sensor_entity_id": _optional_text(
                    source.get("water_sensor_entity_id")
                ),
                "watering_interval_days": interval,
                "last_watered": last.isoformat(),
                "next_watering": next_watering.isoformat(),
                "next_watering_end": next_watering_end.isoformat(),
                "current_season": source.get("current_season")
                or season_for_month(now.month),
                "is_toxic_to_cats": bool(source.get("is_toxic_to_cats", False)),
                "is_toxic_to_dogs": bool(source.get("is_toxic_to_dogs", False)),
                "notes": _optional_text(source.get("notes")),
                **_copy_api_values(source),
                **_copy_schedule_values(source),
            }
        )
    if not plants:
        raise ValueError("No valid plants found")
    return plants


def _clean_values(values: dict[str, Any]) -> dict[str, Any]:
    cleaned = {
        "name": str(values["name"]).strip(),
        "scientific_name": str(values.get("scientific_name", "")).strip() or None,
        "location": str(values.get("location", "")).strip() or None,
        "image_url": str(values.get("image_url", "")).strip() or None,
        "area_id": str(values.get("area_id", "")).strip() or None,
        "water_sensor_entity_id": str(values.get("water_sensor_entity_id", "")).strip()
        or None,
        "watering_interval_days": int(values["watering_interval_days"]),
        "is_toxic_to_cats": bool(values.get("is_toxic_to_cats", False)),
        "is_toxic_to_dogs": bool(values.get("is_toxic_to_dogs", False)),
        "notes": str(values.get("notes", "")).strip() or None,
    }
    cleaned.update(_copy_api_values(values))
    cleaned.update(_copy_schedule_values(values))
    return cleaned


def watering_interval_range(
    plant: dict[str, Any], season: str | None = None
) -> tuple[int, int]:
    """Return the active inclusive watering interval in days."""
    fallback = _bounded_int(
        plant.get("watering_interval_days"), DEFAULT_WATERING_INTERVAL, 1, 365
    )
    default_minimum = _bounded_int(
        plant.get("watering_interval_min_days"), fallback, 1, 365
    )
    default_maximum = _bounded_int(
        plant.get("watering_interval_max_days"), default_minimum, 1, 365
    )
    if plant.get("seasonal_watering_enabled") and season in SEASONS:
        prefix = f"watering_interval_{season}"
        minimum = _bounded_int(plant.get(f"{prefix}_min_days"), default_minimum, 1, 365)
        maximum = _bounded_int(plant.get(f"{prefix}_max_days"), default_maximum, 1, 365)
    else:
        minimum, maximum = default_minimum, default_maximum
    return minimum, max(minimum, maximum)


def season_for_month(month: int) -> str:
    """Return the meteorological season for the northern hemisphere."""
    if month in (3, 4, 5):
        return "spring"
    if month in (6, 7, 8):
        return "summer"
    if month in (9, 10, 11):
        return "autumn"
    return "winter"


def global_reminder_settings(options: dict[str, Any]) -> tuple[bool, str]:
    """Return global reminders while migrating legacy per-plant settings."""
    plants = options.get(CONF_PLANTS, [])
    legacy_plants = plants if isinstance(plants, list) else []
    configured_enabled = options.get(CONF_WATERING_REMINDER_ENABLED)
    enabled = (
        configured_enabled
        if isinstance(configured_enabled, bool)
        else any(
            isinstance(plant, dict) and plant.get("watering_reminder_enabled")
            for plant in legacy_plants
        )
    )
    target = str(options.get(CONF_NOTIFICATION_TARGET) or "").strip()
    if not target:
        target = next(
            (
                str(plant.get("notification_target") or "").strip()
                for plant in legacy_plants
                if isinstance(plant, dict)
                and plant.get("watering_reminder_enabled")
                and plant.get("notification_target")
            ),
            "",
        )
    return bool(enabled), target


def _copy_schedule_values(values: dict[str, Any]) -> dict[str, Any]:
    copied: dict[str, Any] = {}
    for field in _PLANT_TEXT_FIELDS:
        if field in values:
            copied[field] = _optional_text(values.get(field))
    for field in _PLANT_BOOL_FIELDS:
        if field in values:
            copied[field] = bool(values.get(field))
    for field in _PLANT_INT_FIELDS:
        if field in values:
            copied[field] = _optional_int(values.get(field))
    for season in SEASONS:
        for suffix in ("min_days", "max_days"):
            field = f"watering_interval_{season}_{suffix}"
            if field in values:
                copied[field] = _optional_int(values.get(field))
    return copied


def _copy_api_values(values: dict[str, Any]) -> dict[str, Any]:
    copied: dict[str, Any] = {}
    if "perenual_id" in values:
        try:
            copied["perenual_id"] = int(values["perenual_id"])
        except (TypeError, ValueError):
            copied["perenual_id"] = None
    for field in _API_TEXT_FIELDS:
        if field in values:
            copied[field] = _optional_text(values.get(field))
    for field in _API_LIST_FIELDS:
        if field in values:
            source = values.get(field)
            copied[field] = (
                [text for item in source if (text := _optional_text(item))]
                if isinstance(source, list)
                else []
            )
    for field in _API_BOOL_FIELDS:
        if field in values:
            value = values.get(field)
            copied[field] = value if isinstance(value, bool) else None
    return copied


def _valid_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    parsed = dt_util.parse_datetime(value)
    if parsed is not None and parsed.tzinfo is None:
        return parsed.replace(tzinfo=dt_util.UTC)
    return parsed


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).strip() or None


def _optional_int(value: Any) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _bounded_int(value: Any, default: int, minimum: int, maximum: int) -> int:
    parsed = _optional_int(value)
    if parsed is None:
        return default
    return max(minimum, min(maximum, parsed))
