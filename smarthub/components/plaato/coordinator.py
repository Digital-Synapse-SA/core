"""Coordinator for Plaato devices."""

from datetime import timedelta
import logging

from pyplaato.plaato import Plaato, PlaatoDeviceType

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import aiohttp_client
from smarthub.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class PlaatoCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: SmartHub,
        config_entry: ConfigEntry,
        auth_token: str,
        device_type: PlaatoDeviceType,
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        self.api = Plaato(auth_token=auth_token)
        self.hass = hass
        self.device_type = device_type
        self.platforms: list[Platform] = []

        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Update data via library."""
        return await self.api.get_data(
            session=aiohttp_client.async_get_clientsession(self.hass),
            device_type=self.device_type,
        )
