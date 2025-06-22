"""The Starlink integration."""

from __future__ import annotations

from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import StarlinkConfigEntry, StarlinkUpdateCoordinator

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.DEVICE_TRACKER,
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.TIME,
]


async def async_setup_entry(
    hass: SmartHub, config_entry: StarlinkConfigEntry
) -> bool:
    """Set up Starlink from a config entry."""
    config_entry.runtime_data = StarlinkUpdateCoordinator(hass, config_entry)
    await config_entry.runtime_data.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: SmartHub, config_entry: StarlinkConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
