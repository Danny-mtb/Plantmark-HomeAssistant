"""Sidebar panel and WebSocket API for Plantmark."""

from __future__ import annotations

import base64
import binascii
import time
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from typing import Any

import voluptuous as vol
from homeassistant.components import frontend, panel_custom, websocket_api
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import device_registry as dr

from .const import (
    CONF_DEFAULT_WATER_AMOUNT,
    CONF_PLANTS,
    DEFAULT_WATER_AMOUNT,
    DOMAIN,
)
from .plant import new_plant, parse_import, updated_plant

PANEL_URL = "plantmark"
PANEL_ELEMENT = "plantmark-panel"
PANEL_STATIC_URL = "/plantmark_static/plantmark-panel.js"
IMAGE_STATIC_URL = "/plantmark_images"
MAX_IMAGE_BYTES = 2_500_000

_PANEL_REGISTERED = "panel_registered"
_STATIC_REGISTERED = "static_registered"
_WEBSOCKET_REGISTERED = "websocket_registered"

_IMAGE_TYPES = {
    "image/jpeg": (".jpg", (b"\xff\xd8\xff",)),
    "image/png": (".png", (b"\x89PNG\r\n\x1a\n",)),
    "image/webp": (".webp", (b"RIFF",)),
}


async def async_setup_panel(hass: HomeAssistant) -> None:
    """Register the Plantmark sidebar panel and its API once."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    integration_dir = Path(__file__).parent
    image_dir = _image_directory(hass)

    if not domain_data.get(_STATIC_REGISTERED):
        await hass.async_add_executor_job(image_dir.mkdir, 0o755, True, True)
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    PANEL_STATIC_URL,
                    str(integration_dir / "frontend" / "plantmark-panel.js"),
                    False,
                ),
                StaticPathConfig(IMAGE_STATIC_URL, str(image_dir), False),
            ]
        )
        domain_data[_STATIC_REGISTERED] = True

    if not domain_data.get(_WEBSOCKET_REGISTERED):
        for command in (
            websocket_list,
            websocket_save,
            websocket_delete,
            websocket_water,
            websocket_import,
            websocket_settings,
        ):
            websocket_api.async_register_command(hass, command)
        domain_data[_WEBSOCKET_REGISTERED] = True

    if not domain_data.get(_PANEL_REGISTERED):
        await panel_custom.async_register_panel(
            hass,
            frontend_url_path=PANEL_URL,
            webcomponent_name=PANEL_ELEMENT,
            sidebar_title="Plantmark",
            sidebar_icon="mdi:sprout",
            module_url=PANEL_STATIC_URL,
            require_admin=True,
            config_panel_domain=DOMAIN,
        )
        domain_data[_PANEL_REGISTERED] = True


@callback
def async_remove_panel(hass: HomeAssistant) -> None:
    """Remove the sidebar entry while the config entry is unloaded."""
    domain_data = hass.data.get(DOMAIN, {})
    if domain_data.get(_PANEL_REGISTERED):
        frontend.async_remove_panel(hass, PANEL_URL)
        domain_data[_PANEL_REGISTERED] = False


@callback
def async_sync_devices(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Synchronize plant names and selected Home Assistant areas."""
    for plant in entry.options.get(CONF_PLANTS, []):
        if isinstance(plant, dict):
            _sync_device(hass, entry, plant)


@websocket_api.websocket_command({vol.Required("type"): "plantmark/list"})
@websocket_api.require_admin
@callback
def websocket_list(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return plants, areas and settings for the panel."""
    entry = _config_entry(hass)
    area_registry = ar.async_get(hass)
    areas = sorted(
        (
            {"id": area.id, "name": area.name}
            for area in area_registry.async_list_areas()
        ),
        key=lambda item: item["name"].casefold(),
    )
    connection.send_result(
        msg["id"],
        {
            "plants": deepcopy(list(entry.options.get(CONF_PLANTS, []))),
            "areas": areas,
            "settings": {
                CONF_DEFAULT_WATER_AMOUNT: entry.options.get(
                    CONF_DEFAULT_WATER_AMOUNT, DEFAULT_WATER_AMOUNT
                )
            },
        },
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): "plantmark/save",
        vol.Required("plant"): dict,
        vol.Optional("image_data"): str,
        vol.Optional("remove_image", default=False): bool,
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def websocket_save(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Create or update one plant."""
    entry = _config_entry(hass)
    values = dict(msg["plant"])
    plant_id = str(values.get("id") or "")
    plants = deepcopy(list(entry.options.get(CONF_PLANTS, [])))
    existing = next(
        (plant for plant in plants if str(plant.get("id")) == plant_id), None
    )

    _validate_plant_values(hass, values)
    area_id = str(values.get("area_id") or "")
    area = ar.async_get(hass).async_get_area(area_id) if area_id else None
    values["location"] = area.name if area is not None else None
    if existing is None:
        plant = new_plant(values)
        plants.append(plant)
    else:
        values.setdefault("image_url", existing.get("image_url"))
        plant = updated_plant(existing, values)
        plants[plants.index(existing)] = plant

    if msg.get("remove_image"):
        await _async_remove_image(hass, str(plant["id"]))
        plant["image_url"] = None
    elif image_data := msg.get("image_data"):
        plant["image_url"] = await _async_store_image(
            hass, str(plant["id"]), image_data
        )

    _save_plants(hass, entry, plants)
    _sync_device(hass, entry, plant)
    connection.send_result(msg["id"], {"plant": plant})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "plantmark/delete",
        vol.Required("plant_id"): str,
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def websocket_delete(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Delete a plant, its image and its Home Assistant device."""
    entry = _config_entry(hass)
    plant_id = msg["plant_id"]
    plants = [
        plant
        for plant in deepcopy(list(entry.options.get(CONF_PLANTS, [])))
        if str(plant.get("id")) != plant_id
    ]
    if len(plants) == len(entry.options.get(CONF_PLANTS, [])):
        raise HomeAssistantError("Plant not found")

    _save_plants(hass, entry, plants)
    await _async_remove_image(hass, plant_id)
    registry = dr.async_get(hass)
    device = registry.async_get_device(
        identifiers={(DOMAIN, f"{entry.entry_id}_{plant_id}")}
    )
    if device is not None:
        registry.async_remove_device(device.id)
    connection.send_result(msg["id"])


@websocket_api.websocket_command(
    {
        vol.Required("type"): "plantmark/water",
        vol.Required("plant_id"): str,
        vol.Optional("amount_ml"): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=10000)
        ),
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def websocket_water(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Record a watering action from the panel."""
    entry = _config_entry(hass)
    amount = msg.get(
        "amount_ml",
        entry.options.get(CONF_DEFAULT_WATER_AMOUNT, DEFAULT_WATER_AMOUNT),
    )
    await entry.runtime_data.async_water_plant(
        msg["plant_id"], amount_ml=amount if amount > 0 else None
    )
    connection.send_result(msg["id"])


@websocket_api.websocket_command(
    {
        vol.Required("type"): "plantmark/import",
        vol.Required("data"): str,
    }
)
@websocket_api.require_admin
@websocket_api.async_response
async def websocket_import(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Import legacy Plantmark JSON from the panel."""
    entry = _config_entry(hass)
    try:
        imported = parse_import(msg["data"])
    except (TypeError, ValueError) as err:
        raise HomeAssistantError("No valid plants found in the JSON data") from err

    plants = deepcopy(list(entry.options.get(CONF_PLANTS, [])))
    existing_ids = {str(plant.get("id")) for plant in plants}
    added = 0
    for plant in imported:
        plant_id = str(plant.get("id"))
        if plant_id in existing_ids:
            continue
        plants.append(plant)
        existing_ids.add(plant_id)
        added += 1
        _sync_device(hass, entry, plant)
    _save_plants(hass, entry, plants)
    connection.send_result(msg["id"], {"added": added})


@websocket_api.websocket_command(
    {
        vol.Required("type"): "plantmark/settings",
        vol.Required("default_water_amount_ml"): vol.All(
            vol.Coerce(int), vol.Range(min=0, max=10000)
        ),
    }
)
@websocket_api.require_admin
@callback
def websocket_settings(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Update Plantmark-wide settings."""
    entry = _config_entry(hass)
    options = dict(entry.options)
    options[CONF_DEFAULT_WATER_AMOUNT] = msg["default_water_amount_ml"]
    hass.config_entries.async_update_entry(entry, options=options)
    connection.send_result(msg["id"])


def _config_entry(hass: HomeAssistant) -> ConfigEntry:
    entries = hass.config_entries.async_entries(DOMAIN)
    if not entries:
        raise HomeAssistantError("Plantmark is not configured")
    return entries[0]


def _validate_plant_values(hass: HomeAssistant, values: dict[str, Any]) -> None:
    name = str(values.get("name") or "").strip()
    if not name or len(name) > 255:
        raise HomeAssistantError("Plant name must contain 1 to 255 characters")
    try:
        interval = int(values.get("watering_interval_days", 0))
    except (TypeError, ValueError) as err:
        raise HomeAssistantError("Watering interval must be a number") from err
    if not 1 <= interval <= 365:
        raise HomeAssistantError("Watering interval must be between 1 and 365 days")

    area_id = str(values.get("area_id") or "")
    if area_id and ar.async_get(hass).async_get_area(area_id) is None:
        raise HomeAssistantError("Selected Home Assistant area no longer exists")

    sensor = str(values.get("water_sensor_entity_id") or "")
    if sensor and not sensor.startswith(("sensor.", "binary_sensor.")):
        raise HomeAssistantError(
            "Water sensor must be a sensor or binary sensor entity"
        )


@callback
def _save_plants(
    hass: HomeAssistant, entry: ConfigEntry, plants: list[dict[str, Any]]
) -> None:
    options = dict(entry.options)
    options[CONF_PLANTS] = plants
    hass.config_entries.async_update_entry(entry, options=options)
    entry.runtime_data.async_replace_plants(plants)


@callback
def _sync_device(
    hass: HomeAssistant, entry: ConfigEntry, plant: dict[str, Any]
) -> None:
    plant_id = str(plant.get("id") or "")
    if not plant_id:
        return
    registry = dr.async_get(hass)
    device = registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, f"{entry.entry_id}_{plant_id}")},
        manufacturer="Plantmark",
        model=str(plant.get("scientific_name") or "Plant"),
        name=str(plant.get("name") or plant_id),
    )
    area_id = str(plant.get("area_id") or "") or None
    registry.async_update_device(
        device.id,
        area_id=area_id,
        model=str(plant.get("scientific_name") or "Plant"),
        name=str(plant.get("name") or plant_id),
    )


def _image_directory(hass: HomeAssistant) -> Path:
    return Path(hass.config.path("www", DOMAIN))


async def _async_store_image(
    hass: HomeAssistant, plant_id: str, image_data: str
) -> str:
    try:
        header, encoded = image_data.split(",", 1)
        mime_type = header.removeprefix("data:").split(";", 1)[0]
        extension, signatures = _IMAGE_TYPES[mime_type]
        content = base64.b64decode(encoded, validate=True)
    except (ValueError, KeyError, binascii.Error) as err:
        raise HomeAssistantError("Image must be a JPEG, PNG or WebP file") from err

    if not content or len(content) > MAX_IMAGE_BYTES:
        raise HomeAssistantError("Image must not exceed 2.5 MB")
    if not any(content.startswith(signature) for signature in signatures):
        raise HomeAssistantError("Image content does not match its file type")
    if mime_type == "image/webp" and content[8:12] != b"WEBP":
        raise HomeAssistantError("Invalid WebP image")

    await _async_remove_image(hass, plant_id)
    filename = f"{sha256(plant_id.encode()).hexdigest()}{extension}"
    target = _image_directory(hass) / filename
    await hass.async_add_executor_job(target.write_bytes, content)
    return f"{IMAGE_STATIC_URL}/{filename}?v={time.time_ns()}"


async def _async_remove_image(hass: HomeAssistant, plant_id: str) -> None:
    prefix = sha256(plant_id.encode()).hexdigest()
    directory = _image_directory(hass)

    def _remove() -> None:
        for extension, _signatures in _IMAGE_TYPES.values():
            path = directory / f"{prefix}{extension}"
            path.unlink(missing_ok=True)

    await hass.async_add_executor_job(_remove)
