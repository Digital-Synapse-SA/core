"""The dlna_dmr component."""

from __future__ import annotations

from smarthub import config_entries
from smarthub.const import Platform
from smarthub.core import SmartHub

from .const import LOGGER

PLATFORMS = [Platform.MEDIA_PLAYER]


async def async_setup_entry(
    hass: SmartHub, entry: config_entries.ConfigEntry
) -> bool:
    """Set up a DLNA DMR device from a config entry."""
    LOGGER.debug("Setting up config entry: %s", entry.unique_id)

    # Forward setup to the appropriate platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: SmartHub, config_entry: config_entries.ConfigEntry
) -> bool:
    """Unload a config entry."""
    # Forward to the same platform as async_setup_entry did
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
