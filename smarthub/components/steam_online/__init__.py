"""The Steam integration."""

from __future__ import annotations

from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import SteamConfigEntry, SteamDataUpdateCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: SmartHub, entry: SteamConfigEntry) -> bool:
    """Set up Steam from a config entry."""
    coordinator = SteamDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: SteamConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
