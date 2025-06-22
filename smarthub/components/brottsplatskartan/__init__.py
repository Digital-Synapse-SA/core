"""The brottsplatskartan component."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .const import PLATFORMS


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up brottsplatskartan from a config entry."""

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload brottsplatskartan config entry."""

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
