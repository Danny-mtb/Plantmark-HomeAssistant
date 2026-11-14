"""UI configuration and plant management for Plantmark."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr

from .const import (
    CONF_DEFAULT_WATER_AMOUNT,
    CONF_LIBRARY_NAME,
    CONF_PLANTS,
    DEFAULT_LIBRARY_NAME,
    DEFAULT_WATER_AMOUNT,
    DEFAULT_WATERING_INTERVAL,
    DOMAIN,
)
from .plant import new_plant, parse_import, updated_plant

FIELD_PLANT_ID = "plant_id"
FIELD_IMPORT_DATA = "import_data"


class PlantmarkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Create one native Plantmark library."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Create the library; plants are managed through its options flow."""
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            name = user_input[CONF_LIBRARY_NAME].strip() or DEFAULT_LIBRARY_NAME
            return self.async_create_entry(
                title=name,
                data={CONF_LIBRARY_NAME: name},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_LIBRARY_NAME, default=DEFAULT_LIBRARY_NAME
                    ): vol.All(
                        str,
                        vol.Strip,
                        vol.Length(min=1, max=255),
                    )
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Return the plant-management flow."""
        return PlantmarkOptionsFlow()


class PlantmarkOptionsFlow(config_entries.OptionsFlowWithReload):
    """Add, edit, remove and import plants through Home Assistant's UI."""

    _selected_plant_id: str | None = None

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Show the plant-management menu."""
        plants = self._plants
        menu = ["add_plant", "import_plants", "settings"]
        if plants:
            menu[1:1] = ["edit_plant", "remove_plant"]
        return self.async_show_menu(step_id="init", menu_options=menu)

    async def async_step_add_plant(self, user_input: dict[str, Any] | None = None):
        """Add a new plant."""
        if user_input is not None:
            plant = new_plant(user_input)
            return self._save_plants([*self._plants, plant])
        return self.async_show_form(
            step_id="add_plant", data_schema=_plant_schema()
        )

    async def async_step_edit_plant(self, user_input: dict[str, Any] | None = None):
        """Choose a plant to edit."""
        if user_input is not None:
            self._selected_plant_id = user_input[FIELD_PLANT_ID]
            return await self.async_step_edit_plant_details()
        return self.async_show_form(
            step_id="edit_plant",
            data_schema=vol.Schema(
                {vol.Required(FIELD_PLANT_ID): vol.In(self._plant_choices)}
            ),
        )

    async def async_step_edit_plant_details(
        self, user_input: dict[str, Any] | None = None
    ):
        """Edit the selected plant."""
        selected = self._selected_plant
        if selected is None:
            return self.async_abort(reason="plant_not_found")
        if user_input is not None:
            plants = [
                updated_plant(plant, user_input)
                if str(plant.get("id")) == self._selected_plant_id
                else plant
                for plant in self._plants
            ]
            return self._save_plants(plants)
        return self.async_show_form(
            step_id="edit_plant_details",
            data_schema=_plant_schema(selected),
            description_placeholders={"plant": str(selected.get("name", ""))},
        )

    async def async_step_remove_plant(
        self, user_input: dict[str, Any] | None = None
    ):
        """Remove a plant from the library."""
        if user_input is not None:
            plant_id = user_input[FIELD_PLANT_ID]
            plants = [
                plant for plant in self._plants if str(plant.get("id")) != plant_id
            ]
            registry = dr.async_get(self.hass)
            device = registry.async_get_device(
                identifiers={(DOMAIN, f"{self.config_entry.entry_id}_{plant_id}")}
            )
            if device is not None:
                registry.async_remove_device(device.id)
            return self._save_plants(plants)
        return self.async_show_form(
            step_id="remove_plant",
            data_schema=vol.Schema(
                {vol.Required(FIELD_PLANT_ID): vol.In(self._plant_choices)}
            ),
        )

    async def async_step_import_plants(
        self, user_input: dict[str, Any] | None = None
    ):
        """Import plants from a legacy Plantmark JSON response or a JSON list."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                imported = parse_import(user_input[FIELD_IMPORT_DATA])
            except (TypeError, ValueError):
                errors["base"] = "invalid_import"
            else:
                existing_ids = {str(plant.get("id")) for plant in self._plants}
                merged = [*self._plants]
                for plant in imported:
                    plant_id = str(plant.get("id"))
                    if plant_id in existing_ids:
                        continue
                    merged.append(plant)
                    existing_ids.add(plant_id)
                return self._save_plants(merged)

        return self.async_show_form(
            step_id="import_plants",
            data_schema=vol.Schema({vol.Required(FIELD_IMPORT_DATA): str}),
            errors=errors,
        )

    async def async_step_settings(self, user_input: dict[str, Any] | None = None):
        """Configure defaults used when watering plants."""
        if user_input is not None:
            options = dict(self.config_entry.options)
            options.update(user_input)
            return self.async_create_entry(title="", data=options)
        return self.async_show_form(
            step_id="settings",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_DEFAULT_WATER_AMOUNT,
                        default=self.config_entry.options.get(
                            CONF_DEFAULT_WATER_AMOUNT, DEFAULT_WATER_AMOUNT
                        ),
                    ): vol.All(vol.Coerce(int), vol.Range(min=0, max=10000))
                }
            ),
        )

    @property
    def _plants(self) -> list[dict[str, Any]]:
        plants = self.config_entry.options.get(CONF_PLANTS, [])
        return deepcopy(plants) if isinstance(plants, list) else []

    @property
    def _plant_choices(self) -> dict[str, str]:
        return {
            str(plant["id"]): str(plant["name"])
            for plant in self._plants
            if plant.get("id") and plant.get("name")
        }

    @property
    def _selected_plant(self) -> dict[str, Any] | None:
        return next(
            (
                plant
                for plant in self._plants
                if str(plant.get("id")) == self._selected_plant_id
            ),
            None,
        )

    def _save_plants(self, plants: list[dict[str, Any]]):
        options = dict(self.config_entry.options)
        options[CONF_PLANTS] = plants
        return self.async_create_entry(title="", data=options)


def _plant_schema(plant: dict[str, Any] | None = None) -> vol.Schema:
    plant = plant or {}
    return vol.Schema(
        {
            vol.Required("name", default=plant.get("name", "")): vol.All(
                str, vol.Strip, vol.Length(min=1, max=255)
            ),
            vol.Optional(
                "scientific_name", default=plant.get("scientific_name") or ""
            ): str,
            vol.Optional("location", default=plant.get("location") or ""): str,
            vol.Optional("image_url", default=plant.get("image_url") or ""): str,
            vol.Required(
                "watering_interval_days",
                default=plant.get(
                    "watering_interval_days", DEFAULT_WATERING_INTERVAL
                ),
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=365)),
            vol.Required(
                "is_toxic_to_cats", default=plant.get("is_toxic_to_cats", False)
            ): bool,
            vol.Required(
                "is_toxic_to_dogs", default=plant.get("is_toxic_to_dogs", False)
            ): bool,
            vol.Optional("notes", default=plant.get("notes") or ""): str,
        }
    )
