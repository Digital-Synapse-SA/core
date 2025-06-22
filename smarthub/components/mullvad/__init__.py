"""The Mullvad VPN integration."""

import asyncio
from datetime import timedelta
import logging

from mullvad_api import MullvadAPI

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

PLATFORMS = [Platform.BINARY_SENSOR]


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up Mullvad VPN integration."""

    async def async_get_mullvad_api_data():
        async with asyncio.timeout(10):
            api = await hass.async_add_executor_job(MullvadAPI)
            return api.data

    coordinator = DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        config_entry=entry,
        name=DOMAIN,
        update_method=async_get_mullvad_api_data,
        update_interval=timedelta(minutes=1),
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        del hass.data[DOMAIN]

    return unload_ok
