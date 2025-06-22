"""The OpenGarage integration."""

from __future__ import annotations

import opengarage

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_HOST, CONF_PORT, CONF_VERIFY_SSL, Platform
from smarthub.core import SmartHub
from smarthub.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_DEVICE_KEY, DOMAIN
from .coordinator import OpenGarageDataUpdateCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.BUTTON, Platform.COVER, Platform.SENSOR]


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up OpenGarage from a config entry."""
    open_garage_connection = opengarage.OpenGarage(
        f"{entry.data[CONF_HOST]}:{entry.data[CONF_PORT]}",
        entry.data[CONF_DEVICE_KEY],
        entry.data[CONF_VERIFY_SSL],
        async_get_clientsession(hass),
    )
    open_garage_data_coordinator = OpenGarageDataUpdateCoordinator(
        hass, entry, open_garage_connection
    )
    await open_garage_data_coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = open_garage_data_coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
