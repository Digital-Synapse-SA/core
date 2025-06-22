"""The lg_netcast component."""

from typing import Final

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv

from .const import DOMAIN

PLATFORMS: Final[list[Platform]] = [Platform.MEDIA_PLAYER]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup_entry(hass: SmartHub, config_entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    hass.data.setdefault(DOMAIN, {})

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        del hass.data[DOMAIN][entry.entry_id]

    return unload_ok
