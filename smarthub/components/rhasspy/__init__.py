"""The Rhasspy integration."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up Rhasspy from a config entry."""
    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
