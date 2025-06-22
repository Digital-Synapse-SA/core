"""The NYT Games integration."""

from __future__ import annotations

from nyt_games import NYTGamesClient

from smarthub.const import CONF_TOKEN, Platform
from smarthub.core import SmartHub
from smarthub.helpers.aiohttp_client import async_create_clientsession

from .coordinator import NYTGamesConfigEntry, NYTGamesCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(hass: SmartHub, entry: NYTGamesConfigEntry) -> bool:
    """Set up NYTGames from a config entry."""

    client = NYTGamesClient(
        entry.data[CONF_TOKEN], session=async_create_clientsession(hass)
    )

    coordinator = NYTGamesCoordinator(hass, entry, client)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: NYTGamesConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
