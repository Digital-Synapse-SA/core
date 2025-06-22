"""The Minecraft Server integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_ADDRESS, CONF_TYPE
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryNotReady
from smarthub.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    MinecraftServer,
    MinecraftServerAddressError,
    MinecraftServerConnectionError,
    MinecraftServerData,
    MinecraftServerNotInitializedError,
    MinecraftServerType,
)

type MinecraftServerConfigEntry = ConfigEntry[MinecraftServerCoordinator]

SCAN_INTERVAL = timedelta(seconds=60)

_LOGGER = logging.getLogger(__name__)


class MinecraftServerCoordinator(DataUpdateCoordinator[MinecraftServerData]):
    """Minecraft Server data update coordinator."""

    config_entry: MinecraftServerConfigEntry
    _api: MinecraftServer

    def __init__(
        self,
        hass: SmartHub,
        config_entry: MinecraftServerConfigEntry,
    ) -> None:
        """Initialize coordinator instance."""

        super().__init__(
            hass=hass,
            name=config_entry.title,
            config_entry=config_entry,
            logger=_LOGGER,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_setup(self) -> None:
        """Set up the Minecraft Server data coordinator."""

        # Create API instance.
        self._api = MinecraftServer(
            self.hass,
            self.config_entry.data.get(CONF_TYPE, MinecraftServerType.JAVA_EDITION),
            self.config_entry.data[CONF_ADDRESS],
        )

        # Initialize API instance.
        try:
            await self._api.async_initialize()
        except MinecraftServerAddressError as error:
            raise ConfigEntryNotReady(f"Initialization failed: {error}") from error

    async def _async_update_data(self) -> MinecraftServerData:
        """Get updated data from the server."""
        try:
            return await self._api.async_get_data()
        except (
            MinecraftServerConnectionError,
            MinecraftServerNotInitializedError,
        ) as error:
            raise UpdateFailed(error) from error
