"""The Rituals Perfume Genie data update coordinator."""

from datetime import timedelta
import logging

from pyrituals import Diffuser

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class RitualsDataUpdateCoordinator(DataUpdateCoordinator[None]):
    """Class to manage fetching Rituals Perfume Genie device data from single endpoint."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: SmartHub,
        config_entry: ConfigEntry,
        diffuser: Diffuser,
        update_interval: timedelta,
    ) -> None:
        """Initialize global Rituals Perfume Genie data updater."""
        self.diffuser = diffuser
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=f"{DOMAIN}-{diffuser.hublot}",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> None:
        """Fetch data from Rituals."""
        await self.diffuser.update_data()
