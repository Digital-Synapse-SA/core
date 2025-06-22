"""Define an update coordinator for OpenUV."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast

from pyopenuv.errors import InvalidApiKeyError, OpenUvError

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryAuthFailed
from smarthub.helpers.debounce import Debouncer
from smarthub.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import LOGGER

DEFAULT_DEBOUNCER_COOLDOWN_SECONDS = 15 * 60


class OpenUvCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Define an OpenUV data coordinator."""

    config_entry: ConfigEntry
    update_method: Callable[[], Awaitable[dict[str, Any]]]

    def __init__(
        self,
        hass: SmartHub,
        *,
        entry: ConfigEntry,
        name: str,
        latitude: str,
        longitude: str,
        update_method: Callable[[], Awaitable[dict[str, Any]]],
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=entry,
            name=name,
            update_method=update_method,
            request_refresh_debouncer=Debouncer(
                hass,
                LOGGER,
                cooldown=DEFAULT_DEBOUNCER_COOLDOWN_SECONDS,
                immediate=True,
            ),
        )

        self.latitude = latitude
        self.longitude = longitude

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from OpenUV."""
        try:
            data = await self.update_method()
        except InvalidApiKeyError as err:
            raise ConfigEntryAuthFailed("Invalid API key") from err
        except OpenUvError as err:
            raise UpdateFailed(str(err)) from err

        return cast(dict[str, Any], data["result"])
