"""DataUpdateCoordinator for the Tailscale integration."""

from __future__ import annotations

from tailscale import Device, Tailscale, TailscaleAuthenticationError

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_API_KEY
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryAuthFailed
from smarthub.helpers.aiohttp_client import async_get_clientsession
from smarthub.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_TAILNET, DOMAIN, LOGGER, SCAN_INTERVAL


class TailscaleDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Device]]):
    """The Tailscale Data Update Coordinator."""

    config_entry: ConfigEntry

    def __init__(self, hass: SmartHub, config_entry: ConfigEntry) -> None:
        """Initialize the Tailscale coordinator."""
        session = async_get_clientsession(hass)
        self.tailscale = Tailscale(
            session=session,
            api_key=config_entry.data[CONF_API_KEY],
            tailnet=config_entry.data[CONF_TAILNET],
        )

        super().__init__(
            hass,
            LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Device]:
        """Fetch devices from Tailscale."""
        try:
            return await self.tailscale.devices()
        except TailscaleAuthenticationError as err:
            raise ConfigEntryAuthFailed from err
