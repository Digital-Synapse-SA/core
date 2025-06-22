"""The NMBS component."""

import logging

from pyrail import iRail

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.aiohttp_client import async_get_clientsession
from smarthub.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SENSOR]


CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the NMBS component."""

    api_client = iRail(session=async_get_clientsession(hass))

    hass.data.setdefault(DOMAIN, {})
    station_response = await api_client.get_stations()
    if station_response is None:
        return False
    hass.data[DOMAIN] = station_response.stations

    return True


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up NMBS from a config entry."""

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
