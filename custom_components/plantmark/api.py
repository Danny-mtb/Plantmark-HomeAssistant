"""Perenual plant API client for Plantmark."""

from __future__ import annotations

import asyncio
import base64
import re
import time
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import urlsplit

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
MAX_REMOTE_IMAGE_BYTES = 1_500_000
MAX_THUMBNAIL_BYTES = 250_000
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_IMAGE_HOSTS = {"perenual.com", "www.perenual.com"}
ALLOWED_IMAGE_PATHS = ("/storage/species_image/", "/species_image/")

_CLIENT_DATA = "perenual_client"


class PerenualApiError(HomeAssistantError):
    """A safe, user-facing Perenual API error."""


class PerenualClient:
    """Small async Perenual client with an in-memory response cache."""

    def __init__(self, session: ClientSession, api_key: str) -> None:
        self._session = session
        self._api_key = api_key
        self._cache: dict[str, tuple[float, Any]] = {}
        self._image_semaphore = asyncio.Semaphore(4)

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
            results = [
                _search_result(item)
                for item in data[:MAX_RESULTS]
                if isinstance(item, dict) and item.get("id") is not None
            ]
            image_data = await asyncio.gather(
                *(
                    self.async_image_data(
                        result.get("image_url"), max_bytes=MAX_THUMBNAIL_BYTES
                    )
                    for result in results
                )
            )
            for result, encoded_image in zip(results, image_data, strict=True):
                result["image_data"] = encoded_image
            return results

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

    async def async_image_data(
        self, image_url: Any, *, max_bytes: int = MAX_REMOTE_IMAGE_BYTES
    ) -> str | None:
        """Download one trusted Perenual image for use inside Home Assistant."""
        url = _trusted_image_url(image_url)
        if url is None:
            return None

        async def _request() -> str | None:
            async with self._image_semaphore:
                try:
                    async with self._session.get(
                        url,
                        timeout=REQUEST_TIMEOUT,
                        allow_redirects=False,
                    ) as response:
                        content_type = response.headers.get("Content-Type", "").split(
                            ";", 1
                        )[0]
                        if (
                            response.status != 200
                            or content_type not in ALLOWED_IMAGE_TYPES
                        ):
                            return None
                        if (
                            response.content_length is not None
                            and response.content_length > max_bytes
                        ):
                            return None
                        content = await response.content.read(max_bytes + 1)
                        if len(content) > max_bytes:
                            return None
                        encoded = base64.b64encode(content).decode("ascii")
                        return f"data:{content_type};base64,{encoded}"
                except (ClientError, TimeoutError):
                    return None

        return await self._async_cached(
            f"image:{max_bytes}:{url}", DETAIL_CACHE_SECONDS, _request
        )

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
    image = _image_data(payload.get("default_image"), thumbnail=True)
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


def _image_data(value: Any, *, thumbnail: bool = False) -> dict[str, str | None]:
    if not isinstance(value, dict):
        return {
            "image_url": None,
            "image_license_name": None,
            "image_license_url": None,
        }
    return {
        "image_url": _text(
            (value.get("thumbnail") if thumbnail else value.get("medium_url"))
            or value.get("small_url")
            or value.get("regular_url")
            or value.get("original_url")
        ),
        "image_license_name": _text(value.get("license_name")),
        "image_license_url": _text(value.get("license_url")),
    }


def _trusted_image_url(value: Any) -> str | None:
    url = _text(value)
    if url is None:
        return None
    parsed = urlsplit(url)
    try:
        port = parsed.port
    except ValueError:
        return None
    if (
        parsed.scheme != "https"
        or parsed.hostname not in ALLOWED_IMAGE_HOSTS
        or not parsed.path.startswith(ALLOWED_IMAGE_PATHS)
        or parsed.username is not None
        or parsed.password is not None
        or port not in (None, 443)
    ):
        return None
    return url


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
