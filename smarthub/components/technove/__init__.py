"""The TechnoVE integration."""

from __future__ import annotations

from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import TechnoVEConfigEntry, TechnoVEDataUpdateCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.NUMBER, Platform.SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: SmartHub, entry: TechnoVEConfigEntry) -> bool:
    """Set up TechnoVE from a config entry."""
    coordinator = TechnoVEDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: TechnoVEConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
