"""Support for Roku."""

from __future__ import annotations

from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import RokuConfigEntry, RokuDataUpdateCoordinator

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.MEDIA_PLAYER,
    Platform.REMOTE,
    Platform.SELECT,
    Platform.SENSOR,
]


async def async_setup_entry(hass: SmartHub, entry: RokuConfigEntry) -> bool:
    """Set up Roku from a config entry."""
    coordinator = RokuDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: SmartHub, entry: RokuConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: SmartHub, entry: RokuConfigEntry) -> None:
    """Reload the config entry when it changed."""
    await hass.config_entries.async_reload(entry.entry_id)
