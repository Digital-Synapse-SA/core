"""The Airthings integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from airthings import Airthings

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_ID, Platform
from smarthub.core import SmartHub
from smarthub.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_SECRET
from .coordinator import AirthingsDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]
SCAN_INTERVAL = timedelta(minutes=6)

type AirthingsConfigEntry = ConfigEntry[AirthingsDataUpdateCoordinator]


async def async_setup_entry(hass: SmartHub, entry: AirthingsConfigEntry) -> bool:
    """Set up Airthings from a config entry."""
    airthings = Airthings(
        entry.data[CONF_ID],
        entry.data[CONF_SECRET],
        async_get_clientsession(hass),
    )

    coordinator = AirthingsDataUpdateCoordinator(hass, airthings)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: AirthingsConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
