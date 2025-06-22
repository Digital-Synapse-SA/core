"""The Dune HD component."""

from __future__ import annotations

from typing import Final

from pdunehd import DuneHDPlayer

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_HOST, Platform
from smarthub.core import SmartHub

PLATFORMS: Final[list[Platform]] = [Platform.MEDIA_PLAYER]


type DuneHDConfigEntry = ConfigEntry[DuneHDPlayer]


async def async_setup_entry(hass: SmartHub, entry: DuneHDConfigEntry) -> bool:
    """Set up a config entry."""
    entry.runtime_data = DuneHDPlayer(entry.data[CONF_HOST])

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: DuneHDConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
