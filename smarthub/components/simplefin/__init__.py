"""The SimpleFIN integration."""

from __future__ import annotations

from simplefin4py import SimpleFin

from smarthub.const import Platform
from smarthub.core import SmartHub

from .const import CONF_ACCESS_URL
from .coordinator import SimpleFinConfigEntry, SimpleFinDataUpdateCoordinator

PLATFORMS: list[str] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]


async def async_setup_entry(hass: SmartHub, entry: SimpleFinConfigEntry) -> bool:
    """Set up from a config entry."""
    access_url = entry.data[CONF_ACCESS_URL]
    sf_client = SimpleFin(access_url)
    sf_coordinator = SimpleFinDataUpdateCoordinator(hass, entry, sf_client)
    await sf_coordinator.async_config_entry_first_refresh()
    entry.runtime_data = sf_coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: SimpleFinConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
