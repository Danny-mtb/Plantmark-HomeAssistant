"""Perenual plant API client for Plantmark."""

from __future__ import annotations

import asyncio
import base64
import html
import ipaddress
import json
import logging
import re
import time
from collections.abc import Awaitable, Callable
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlsplit

from aiohttp import ClientError, ClientSession, ClientTimeout
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import dt as dt_util

from .const import DOMAIN

API_BASE_URL = "https://www.perenual.com/api/v2"
CARE_GUIDE_URL = "https://www.perenual.com/api/species-care-guide-list"
PUBLIC_PLANT_URL = (
    "https://www.perenual.com/plant-species-database-search-finder/species"
)
REQUEST_TIMEOUT = ClientTimeout(total=20)
PUBLIC_PAGE_TIMEOUT = ClientTimeout(total=15)
SEARCH_CACHE_SECONDS = 30 * 60
DETAIL_CACHE_SECONDS = 24 * 60 * 60
MAX_RESULTS = 20
MAX_REMOTE_IMAGE_BYTES = 1_500_000
MAX_THUMBNAIL_BYTES = 250_000
MAX_PUBLIC_PAGE_BYTES = 2_000_000
ALLOWED_IMAGE_HOSTS = {"perenual.com", "www.perenual.com"}
ALLOWED_IMAGE_PATHS = ("/storage/species_image/", "/species_image/")

_CLIENT_DATA = "perenual_client"
_LOGGER = logging.getLogger(__name__)


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
        """Load and merge botanical details with the separate care guide."""
        cache_key = f"details:{species_id}"

        async def _request() -> dict[str, Any]:
            detail_result, guide_result = await asyncio.gather(
                self._async_get(f"species/details/{species_id}"),
                self._async_get_url(CARE_GUIDE_URL, {"species_id": species_id}),
                return_exceptions=True,
            )
            details: dict[str, Any] = {}
            errors: list[PerenualApiError] = []
            if isinstance(detail_result, Exception):
                if isinstance(detail_result, PerenualApiError):
                    errors.append(detail_result)
            elif (
                isinstance(detail_result, dict)
                and detail_result.get("id") is not None
            ):
                details.update(_plant_details(detail_result))
            guide = (
                _care_guide_data(guide_result, species_id)
                if isinstance(guide_result, dict)
                else {}
            )
            if isinstance(guide_result, Exception):
                _LOGGER.debug(
                    "Perenual care-guide API unavailable for species %s: %s",
                    species_id,
                    guide_result,
                )
            if "watering_guide" not in guide:
                public_guide = await self._async_public_care_guide(species_id)
                public_guide.update(guide)
                guide = public_guide
            details.update(guide)
            if details:
                details.setdefault("api_provider", "perenual")
                details.setdefault("perenual_id", species_id)
                details.setdefault("perenual_url", _perenual_url(species_id))
                details.setdefault("api_last_synced", dt_util.now().isoformat())
                return details
            if errors:
                raise errors[0]
            raise PerenualApiError("Perenual returned no plant care data")

        return await self._async_cached(cache_key, DETAIL_CACHE_SECONDS, _request)

    async def _async_public_care_guide(self, species_id: int) -> dict[str, Any]:
        """Read care guidance from Perenual's public species page as fallback."""
        try:
            async with self._session.get(
                f"{PUBLIC_PLANT_URL}/{species_id}",
                timeout=PUBLIC_PAGE_TIMEOUT,
                allow_redirects=True,
                max_redirects=3,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (X11; Linux x86_64) "
                        "AppleWebKit/537.36 Chrome/140 Safari/537.36"
                    )
                },
            ) as response:
                final_url = urlsplit(str(response.url))
                if (
                    response.status != 200
                    or final_url.scheme != "https"
                    or final_url.hostname not in ALLOWED_IMAGE_HOSTS
                ):
                    _LOGGER.debug(
                        "Perenual public page unavailable for species %s: %s",
                        species_id,
                        response.status,
                    )
                    return {}
                content_type = response.headers.get("Content-Type", "")
                if "text/html" not in content_type.casefold():
                    return {}
                if (
                    response.content_length is not None
                    and response.content_length > MAX_PUBLIC_PAGE_BYTES
                ):
                    return {}
                content = await response.content.read(MAX_PUBLIC_PAGE_BYTES + 1)
                if len(content) > MAX_PUBLIC_PAGE_BYTES:
                    return {}
                guide = _public_care_guide_data(
                    content.decode(response.charset or "utf-8", errors="replace")
                )
                if not guide:
                    _LOGGER.debug(
                        "No care guidance found on public Perenual page for %s",
                        species_id,
                    )
                return guide
        except (ClientError, TimeoutError, UnicodeError, LookupError) as err:
            _LOGGER.debug(
                "Unable to read public Perenual page for species %s: %s",
                species_id,
                err,
            )
            return {}

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
                        allow_redirects=True,
                        max_redirects=3,
                    ) as response:
                        if response.status != 200 or not _safe_image_response_url(
                            str(response.url)
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
                        content_type = _detected_image_type(content)
                        if content_type is None:
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
        return await self._async_get_url(f"{API_BASE_URL}/{path}", parameters)

    async def _async_get_url(
        self, url: str, parameters: dict[str, Any] | None = None
    ) -> Any:
        """Request one of Perenual's official API endpoints."""
        params = {"key": self._api_key, **(parameters or {})}
        try:
            async with self._session.get(
                url, params=params, timeout=REQUEST_TIMEOUT
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
    result = _normalized_plant_data(payload)
    result.update(
        {
            "id": int(payload["id"]),
            "api_provider": "perenual",
            "perenual_id": int(payload["id"]),
            "perenual_url": _perenual_url(payload["id"]),
            "api_last_synced": dt_util.now().isoformat(),
            **image,
        }
    )
    minimum, maximum = _watering_interval_range(
        payload.get("watering_general_benchmark")
    )
    estimated = False
    if minimum is None:
        minimum, maximum = _watering_category_range(payload.get("watering"))
        estimated = minimum is not None
    result.update(
        {
            "watering_interval_days": minimum,
            "watering_interval_min_days": minimum,
            "watering_interval_max_days": maximum,
            "watering_interval_estimated": estimated,
        }
    )
    return result


def _plant_details(payload: dict[str, Any]) -> dict[str, Any]:
    image = _image_data(payload.get("default_image"))
    watering_minimum, watering_maximum = _watering_interval_range(
        payload.get("watering_general_benchmark")
    )
    return {
        **_normalized_plant_data(payload),
        "api_provider": "perenual",
        "perenual_id": int(payload["id"]),
        "perenual_url": _perenual_url(payload["id"]),
        "api_last_synced": dt_util.now().isoformat(),
        "watering_interval_days": watering_minimum,
        "watering_interval_min_days": watering_minimum,
        "watering_interval_max_days": watering_maximum,
        "watering_interval_estimated": False,
        **image,
    }


def _care_guide_data(payload: dict[str, Any], species_id: int) -> dict[str, Any]:
    """Normalize the independent Perenual plant-guide response."""
    data = payload.get("data")
    if not isinstance(data, list):
        return {}
    record = next(
        (
            item
            for item in data
            if isinstance(item, dict)
            and _optional_int(item.get("species_id")) == species_id
        ),
        None,
    )
    if not isinstance(record, dict) or not isinstance(record.get("section"), list):
        return {}

    guides: dict[str, str] = {}
    for section in record["section"]:
        if not isinstance(section, dict):
            continue
        guide_type = _text(section.get("type"))
        description = _text(section.get("description"))
        if guide_type and description:
            guides[guide_type.casefold()] = description

    return _normalized_guides(guides)


def _normalized_guides(guides: dict[str, str]) -> dict[str, Any]:
    """Convert care-guide sections and any explicit watering interval."""
    normalized: dict[str, Any] = {
        f"{guide_type}_guide": description
        for guide_type, description in guides.items()
        if guide_type in {"watering", "sunlight", "pruning"}
    }
    watering_minimum, watering_maximum = _interval_from_watering_guide(
        guides.get("watering")
    )
    if watering_minimum is not None:
        normalized.update(
            {
                "watering_interval_days": watering_minimum,
                "watering_interval_min_days": watering_minimum,
                "watering_interval_max_days": watering_maximum,
                "watering_interval_estimated": False,
                "watering_interval_source": "care_guide",
            }
        )
    return normalized


class _CarePageParser(HTMLParser):
    """Collect headings, paragraphs and JSON scripts from a public plant page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[tuple[str, str]] = []
        self.scripts: list[str] = []
        self._tag: str | None = None
        self._parts: list[str] = []
        self._script_parts: list[str] | None = None

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag == "script":
            self._script_parts = []
        elif self._tag is None and tag in {"p", "li", "h1", "h2", "h3", "h4"}:
            self._tag = tag
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._script_parts is not None:
            self._script_parts.append(data)
        elif self._tag is not None:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._script_parts is not None:
            self.scripts.append("".join(self._script_parts))
            self._script_parts = None
        elif tag == self._tag:
            text = _compact_text(" ".join(self._parts))
            if text:
                self.blocks.append((tag, text))
            self._tag = None
            self._parts = []


def _public_care_guide_data(source: str) -> dict[str, Any]:
    """Extract care sections from rendered HTML or embedded page JSON."""
    parser = _CarePageParser()
    try:
        parser.feed(source)
    except (ValueError, AssertionError):
        return {}

    guides: dict[str, str] = {}
    for index, (tag, heading) in enumerate(parser.blocks):
        guide_type = heading.casefold().strip(" :")
        if tag not in {"h1", "h2", "h3", "h4"} or guide_type not in {
            "watering",
            "sunlight",
            "pruning",
        }:
            continue
        paragraphs: list[str] = []
        for next_tag, text in parser.blocks[index + 1 :]:
            if next_tag in {"h1", "h2", "h3", "h4"}:
                break
            if next_tag in {"p", "li"}:
                paragraphs.append(text)
        description = _compact_text("\n\n".join(paragraphs))
        if len(description) >= 40:
            guides[guide_type] = description

    for script in parser.scripts:
        _collect_embedded_guides(script, guides)

    if "watering" not in guides:
        candidates = [
            text
            for tag, text in parser.blocks
            if tag in {"p", "li"} and _looks_like_watering_guide(text)
        ]
        if candidates:
            guides["watering"] = max(candidates, key=len)
    return _normalized_guides(guides)


def _collect_embedded_guides(source: str, guides: dict[str, str]) -> None:
    """Find care descriptions in JSON and Next.js embedded strings."""
    queue: list[Any] = []
    try:
        queue.append(json.loads(source))
    except (json.JSONDecodeError, TypeError):
        pass
    for match in re.finditer(r'"((?:\\.|[^"\\]){40,})"', source):
        try:
            queue.append(json.loads(f'"{match.group(1)}"'))
        except json.JSONDecodeError:
            continue

    while queue:
        value = queue.pop()
        if isinstance(value, dict):
            guide_type = str(value.get("type") or "").casefold()
            description = _compact_text(value.get("description"))
            if guide_type in {"watering", "sunlight", "pruning"} and len(
                description
            ) >= 40:
                guides.setdefault(guide_type, description)
            queue.extend(value.values())
        elif isinstance(value, list):
            queue.extend(value)
        elif isinstance(value, str) and _looks_like_watering_guide(value):
            guides.setdefault("watering", _compact_text(value))


def _looks_like_watering_guide(value: Any) -> bool:
    text = _compact_text(value)
    lowered = text.casefold()
    return (
        len(text) >= 60
        and any(word in lowered for word in ("water", "watering"))
        and any(word in lowered for word in ("soil", "days", "weeks", "moist"))
    )


def _compact_text(value: Any) -> str:
    return re.sub(r"[ \t\r\f\v]+", " ", html.unescape(str(value or ""))).strip()


def _normalized_plant_data(payload: dict[str, Any]) -> dict[str, Any]:
    """Return all useful care fields available in a search or detail response."""
    return {
        "common_name": _text(payload.get("common_name")),
        "scientific_name": _first_text(payload.get("scientific_name")),
        "other_names": _text_list(payload.get("other_name")),
        "family": _text(payload.get("family")),
        "origin": _text_list(payload.get("origin")),
        "plant_type": _text(payload.get("type")),
        "cycle": _text(payload.get("cycle")),
        "watering": _text(payload.get("watering")),
        "watering_quality": _text(payload.get("watering_quality")),
        "watering_period": _joined_text(payload.get("watering_period")),
        "water_depth_requirement": _measurement_text(
            payload.get("depth_water_requirement")
        ),
        "water_volume_requirement": _measurement_text(
            payload.get("volume_water_requirement")
        ),
        "average_volume_requirement": _measurement_text(
            payload.get("average_volume_requirement")
            or payload.get("average_volume_requirements")
        ),
        "base_temperature": _measurement_text(payload.get("base_temperature")),
        "ph_level": _measurement_text(payload.get("ph_level")),
        "sunlight_duration": _measurement_text(payload.get("sunlight_duration")),
        "temperature_tolerance": _measurement_text(
            payload.get("temperature_tolerance")
            or payload.get("temperature_tolerence")
        ),
        "spacing_requirement": _measurement_text(
            payload.get("spacing_requirement")
            or payload.get("spacing_requirements")
        ),
        "sunlight": _text_list(payload.get("sunlight")),
        "soil": _text_list(payload.get("soil")),
        "care_level": _text(payload.get("care_level")),
        "description": _text(payload.get("description")),
        "growth_rate": _text(payload.get("growth_rate")),
        "maintenance": _text(payload.get("maintenance")),
        "hardiness_min": _nested_text(payload.get("hardiness"), "min"),
        "hardiness_max": _nested_text(payload.get("hardiness"), "max"),
        "flowering_season": _text(payload.get("flowering_season")),
        "fruiting_season": _text(payload.get("fruiting_season")),
        "harvest_season": _text(payload.get("harvest_season")),
        "harvest_method": _text(payload.get("harvest_method")),
        "dimensions": _measurement_text(payload.get("dimensions")),
        "pruning_frequency": _measurement_text(payload.get("pruning_count")),
        "seeds": _text(payload.get("seeds")),
        "propagation": _text_list(payload.get("propagation")),
        "attracts": _text_list(payload.get("attracts")),
        "pruning_month": _text_list(payload.get("pruning_month")),
        "pest_susceptibility": _text_list(payload.get("pest_susceptibility")),
        "flower_color": _text_list(payload.get("flower_color")),
        "fruit_color": _text_list(payload.get("fruit_color")),
        **{
            field: _optional_bool(payload.get(field))
            for field in (
                "indoor",
                "poisonous_to_humans",
                "poisonous_to_pets",
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
        },
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


def _safe_image_response_url(value: str) -> bool:
    """Reject unsafe redirect targets while allowing Perenual's image cloud."""
    parsed = urlsplit(value)
    try:
        port = parsed.port
    except ValueError:
        return False
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or port not in (None, 443)
    ):
        return False
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError:
        return True
    return address.is_global


def _detected_image_type(content: bytes) -> str | None:
    """Detect supported images by their bytes instead of unreliable headers."""
    if content.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP":
        return "image/webp"
    return None


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


def _watering_category_range(value: Any) -> tuple[int | None, int | None]:
    """Map Perenual's broad search category to a conservative estimate."""
    ranges = {
        "frequent": (3, 5),
        "average": (7, 10),
        "minimum": (14, 21),
        "none": (30, 60),
    }
    return ranges.get(str(value or "").strip().casefold(), (None, None))


def _interval_from_watering_guide(value: Any) -> tuple[int | None, int | None]:
    """Extract only an explicit every-N-days/weeks/months guide statement."""
    text = _text(value)
    if text is None:
        return None, None
    match = re.search(
        r"(?:once\s+)?every\s+(\d+)\s*(?:[-–—]|to)?\s*(\d+)?\s*"
        r"(day|week|month)s?\b",
        text,
        flags=re.IGNORECASE,
    )
    if match is None:
        return None, None
    minimum = int(match.group(1))
    maximum = int(match.group(2) or minimum)
    multiplier = {"day": 1, "week": 7, "month": 30}[match.group(3).casefold()]
    minimum = max(1, min(365, minimum * multiplier))
    maximum = max(minimum, min(365, maximum * multiplier))
    return minimum, maximum


def _nested_text(value: Any, key: str) -> str | None:
    return _text(value.get(key)) if isinstance(value, dict) else None


def _measurement_text(value: Any) -> str | None:
    """Format Perenual's small measurement/count objects for local storage."""
    if not isinstance(value, dict):
        return _text(value)
    parts: list[str] = []
    minimum = _text(value.get("min_value") or value.get("min"))
    maximum = _text(value.get("max_value") or value.get("max"))
    scalar = _text(value.get("value") or value.get("amount"))
    if minimum or maximum:
        parts.append("–".join(item for item in (minimum, maximum) if item))
    elif scalar:
        parts.append(scalar)
    unit = _text(value.get("unit") or value.get("interval"))
    if unit:
        parts.append(unit)
    return " ".join(parts) or None


def _joined_text(value: Any) -> str | None:
    values = _text_list(value)
    return ", ".join(values) or None


def _optional_bool(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def _optional_int(value: Any) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _perenual_url(species_id: Any) -> str:
    return (
        "https://www.perenual.com/plant-species-database-search-finder/species/"
        f"{int(species_id)}"
    )


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
