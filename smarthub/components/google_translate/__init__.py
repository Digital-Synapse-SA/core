"""The Google Translate text-to-speech integration."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub

PLATFORMS: list[Platform] = [Platform.TTS]


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up Google Translate text-to-speech from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
