"""Data update coordinator for the Tautulli integration."""

from __future__ import annotations

import asyncio
from datetime import timedelta

from pytautulli import (
    PyTautulli,
    PyTautulliApiActivity,
    PyTautulliApiHomeStats,
    PyTautulliApiUser,
)
from pytautulli.exceptions import (
    PyTautulliAuthenticationException,
    PyTautulliConnectionException,
)
from pytautulli.models.host_configuration import PyTautulliHostConfiguration

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryAuthFailed
from smarthub.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER

type TautulliConfigEntry = ConfigEntry[TautulliDataUpdateCoordinator]


class TautulliDataUpdateCoordinator(DataUpdateCoordinator[None]):
    """Data update coordinator for the Tautulli integration."""

    config_entry: TautulliConfigEntry

    def __init__(
        self,
        hass: SmartHub,
        config_entry: TautulliConfigEntry,
        host_configuration: PyTautulliHostConfiguration,
        api_client: PyTautulli,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(seconds=10),
        )
        self.host_configuration = host_configuration
        self.api_client = api_client
        self.activity: PyTautulliApiActivity | None = None
        self.home_stats: list[PyTautulliApiHomeStats] | None = None
        self.users: list[PyTautulliApiUser] | None = None

    async def _async_update_data(self) -> None:
        """Get the latest data from Tautulli."""
        try:
            [self.activity, self.home_stats, self.users] = await asyncio.gather(
                *[
                    self.api_client.async_get_activity(),
                    self.api_client.async_get_home_stats(),
                    self.api_client.async_get_users(),
                ]
            )
        except PyTautulliConnectionException as ex:
            raise UpdateFailed(ex) from ex
        except PyTautulliAuthenticationException as ex:
            raise ConfigEntryAuthFailed(ex) from ex
