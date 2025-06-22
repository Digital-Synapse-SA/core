"""The coordinator for the Youless integration."""

from datetime import timedelta
import logging

from youless_api import YoulessAPI

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class YouLessCoordinator(DataUpdateCoordinator[None]):
    """Class to manage fetching YouLess data."""

    config_entry: ConfigEntry

    def __init__(
        self, hass: SmartHub, config_entry: ConfigEntry, device: YoulessAPI
    ) -> None:
        """Initialize global YouLess data provider."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name="youless_gateway",
            update_interval=timedelta(seconds=10),
        )
        self.device = device

    async def _async_update_data(self) -> None:
        await self.hass.async_add_executor_job(self.device.update)
