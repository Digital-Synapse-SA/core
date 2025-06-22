"""The Flexit Nordic (BACnet) integration."""

from __future__ import annotations

from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import FlexitConfigEntry, FlexitCoordinator

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: SmartHub, entry: FlexitConfigEntry) -> bool:
    """Set up Flexit Nordic (BACnet) from a config entry."""

    coordinator = FlexitCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: FlexitConfigEntry) -> bool:
    """Unload the Flexit Nordic (BACnet) config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
