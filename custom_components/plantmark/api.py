"""Perenual plant API client for Plantmark."""

from __future__ import annotations

import re
import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiohttp import ClientError, ClientSession, ClientTimeout
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util

from .const import DOMAIN

API_BASE_URL = "https://www.perenual.com/api/v2"
REQUEST_TIMEOUT = ClientTimeout(total=20)
SEARCH_CACHE_SECONDS = 30 * 60
DETAIL_CACHE_SECONDS = 24 * 60 * 60
MAX_RESULTS = 20

_CLIENT_DATA = "perenual_client"


class PerenualApiError(HomeAssistantError):
    """A safe, user-facing Perenual API error."""


class PerenualClient:
    """Small async Perenual client with an in-memory response cache."""

    def __init__(self, session: ClientSession, api_key: str) -> None:
        self._session = session
        self._api_key = api_key
        self._cache: dict[str, tuple[float, Any]] = {}

    @property
    def api_key(self) -> str:
        """Return the key only for comparing cached client instances."""
        return self._api_key

    async def async_search(self, query: str) -> list[dict[str, Any]]:
        """Search plants by common or scientific name."""
        normalized = query.strip()
        cache_key = f"search:{normalized.casefold()}"

        async def _request() -> list[dict[str, Any]]:
            payload = await self._async_get("species-list", {"q": normalized})
            data = payload.get("data", []) if isinstance(payload, dict) else []
            if not isinstance(data, list):
                return []
            return [
                _search_result(item)
                for item in data[:MAX_RESULTS]
                if isinstance(item, dict) and item.get("id") is not None
            ]

        return await self._async_cached(cache_key, SEARCH_CACHE_SECONDS, _request)

    async def async_details(self, species_id: int) -> dict[str, Any]:
        """Load normalized plant care data for one species."""
        cache_key = f"details:{species_id}"

        async def _request() -> dict[str, Any]:
            payload = await self._async_get(f"species/details/{species_id}")
            if not isinstance(payload, dict) or payload.get("id") is None:
                raise PerenualApiError("Perenual returned invalid plant details")
            return _plant_details(payload)

        return await self._async_cached(cache_key, DETAIL_CACHE_SECONDS, _request)

    async def _async_get(
        self, path: str, parameters: dict[str, Any] | None = None
    ) -> Any:
        params = {"key": self._api_key, **(parameters or {})}
        try:
            async with self._session.get(
                f"{API_BASE_URL}/{path}", params=params, timeout=REQUEST_TIMEOUT
            ) as response:
                if response.status in (401, 403):
                    raise PerenualApiError("The Perenual API key is invalid")
                if response.status == 404:
                    raise PerenualApiError("The plant was not found by Perenual")
                if response.status == 429:
                    raise PerenualApiError(
                        "The Perenual request limit has been reached"
                    )
                if response.status >= 400:
                    raise PerenualApiError(
                        f"Perenual request failed with status {response.status}"
                    )
                return await response.json(content_type=None)
        except PerenualApiError:
            raise
        except (ClientError, TimeoutError, ValueError) as err:
            raise PerenualApiError("Perenual is currently unavailable") from err

    async def _async_cached(
        self,
        cache_key: str,
        lifetime: int,
        request: Callable[[], Awaitable[Any]],
    ) -> Any:
        cached = self._cache.get(cache_key)
        if cached is not None and time.monotonic() - cached[0] < lifetime:
            return cached[1]
        result = await request()
        self._cache[cache_key] = (time.monotonic(), result)
        return result


@callback
def get_perenual_client(hass: HomeAssistant, api_key: str) -> PerenualClient:
    """Return a client tied to the currently configured API key."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    client = domain_data.get(_CLIENT_DATA)
    if isinstance(client, PerenualClient) and client.api_key == api_key:
        return client
    client = PerenualClient(async_get_clientsession(hass), api_key)
    domain_data[_CLIENT_DATA] = client
    return client


@callback
def clear_perenual_client(hass: HomeAssistant) -> None:
    """Discard cached API data after the key changes."""
    hass.data.setdefault(DOMAIN, {}).pop(_CLIENT_DATA, None)


def _search_result(payload: dict[str, Any]) -> dict[str, Any]:
    image = _image_data(payload.get("default_image"))
    return {
        "id": int(payload["id"]),
        "common_name": _text(payload.get("common_name")),
        "scientific_name": _first_text(payload.get("scientific_name")),
        "other_names": _text_list(payload.get("other_name")),
        "cycle": _text(payload.get("cycle")),
        "watering": _text(payload.get("watering")),
        "sunlight": _text_list(payload.get("sunlight")),
        "indoor": payload.get("indoor")
        if isinstance(payload.get("indoor"), bool)
        else None,
        **image,
    }


def _plant_details(payload: dict[str, Any]) -> dict[str, Any]:
    image = _image_data(payload.get("default_image"))
    poisonous_pets = payload.get("poisonous_to_pets")
    poisonous_humans = payload.get("poisonous_to_humans")
    watering_minimum, watering_maximum = _watering_interval_range(
        payload.get("watering_general_benchmark")
    )
    return {
        "api_provider": "perenual",
        "perenual_id": int(payload["id"]),
        "api_last_synced": dt_util.now().isoformat(),
        "common_name": _text(payload.get("common_name")),
        "scientific_name": _first_text(payload.get("scientific_name")),
        "other_names": _text_list(payload.get("other_name")),
        "family": _text(payload.get("family")),
        "origin": _text_list(payload.get("origin")),
        "plant_type": _text(payload.get("type")),
        "cycle": _text(payload.get("cycle")),
        "watering": _text(payload.get("watering")),
        "watering_interval_days": watering_minimum,
        "watering_interval_min_days": watering_minimum,
        "watering_interval_max_days": watering_maximum,
        "sunlight": _text_list(payload.get("sunlight")),
        "soil": _text_list(payload.get("soil")),
        "care_level": _text(payload.get("care_level")),
        "description": _text(payload.get("description")),
        "poisonous_to_pets": (
            poisonous_pets if isinstance(poisonous_pets, bool) else None
        ),
        "poisonous_to_humans": (
            poisonous_humans if isinstance(poisonous_humans, bool) else None
        ),
        "indoor": payload.get("indoor")
        if isinstance(payload.get("indoor"), bool)
        else None,
        **image,
    }


def _image_data(value: Any) -> dict[str, str | None]:
    if not isinstance(value, dict):
        return {
            "image_url": None,
            "image_license_name": None,
            "image_license_url": None,
        }
    return {
        "image_url": _text(
            value.get("regular_url")
            or value.get("medium_url")
            or value.get("small_url")
            or value.get("original_url")
        ),
        "image_license_name": _text(value.get("license_name")),
        "image_license_url": _text(value.get("license_url")),
    }


def _watering_interval_range(value: Any) -> tuple[int | None, int | None]:
    if not isinstance(value, dict):
        return None, None
    unit = str(value.get("unit") or "").casefold()
    numbers = [
        int(number) for number in re.findall(r"\d+", str(value.get("value", "")))
    ]
    if not numbers:
        return None, None
    multiplier = 1
    if "week" in unit:
        multiplier = 7
    elif "month" in unit:
        multiplier = 30
    elif unit and "day" not in unit:
        return None, None
    minimum = max(1, min(365, min(numbers) * multiplier))
    maximum = max(minimum, min(365, max(numbers) * multiplier))
    return minimum, maximum


def _first_text(value: Any) -> str | None:
    if isinstance(value, list):
        return next((_text(item) for item in value if _text(item)), None)
    return _text(value)


def _text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        text = _text(value)
        return [text] if text else []
    return [text for item in value if (text := _text(item))]


def _text(value: Any) -> str | None:
    if value is None:
        return None
    return str(value).strip() or None
