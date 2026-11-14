"""Plant data normalization shared by the config flow and sidebar panel."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from homeassistant.util import dt as dt_util

from .const import DEFAULT_WATERING_INTERVAL


def new_plant(values: dict[str, Any]) -> dict[str, Any]:
    """Create a normalized plant with its first watering schedule."""
    now = dt_util.now()
    interval = int(values["watering_interval_days"])
    return {
        "id": uuid4().hex,
        **_clean_values(values),
        "last_watered": now.isoformat(),
        "next_watering": (now + timedelta(days=interval)).isoformat(),
        "current_season": _current_season(now.month),
    }


def updated_plant(plant: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    """Apply normalized changes while retaining panel-only legacy data."""
    cleaned = _clean_values(values)
    for panel_field in ("area_id", "water_sensor_entity_id"):
        if panel_field not in values:
            cleaned.pop(panel_field, None)
    updated = {**plant, **cleaned}
    last_watered = dt_util.parse_datetime(str(updated.get("last_watered", "")))
    if last_watered is not None:
        updated["next_watering"] = (
            last_watered + timedelta(days=int(updated["watering_interval_days"]))
        ).isoformat()
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
        next_watering = _valid_datetime(source.get("next_watering")) or (
            last + timedelta(days=interval)
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
                "current_season": source.get("current_season")
                or _current_season(now.month),
                "is_toxic_to_cats": bool(source.get("is_toxic_to_cats", False)),
                "is_toxic_to_dogs": bool(source.get("is_toxic_to_dogs", False)),
                "notes": _optional_text(source.get("notes")),
            }
        )
    if not plants:
        raise ValueError("No valid plants found")
    return plants


def _clean_values(values: dict[str, Any]) -> dict[str, Any]:
    return {
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


def _current_season(month: int) -> str:
    return "summer" if 4 <= month <= 9 else "winter"
