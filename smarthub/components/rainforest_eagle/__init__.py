"""The Rainforest Eagle integration."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub

from .const import DOMAIN
from .coordinator import EagleDataCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up Rainforest Eagle from a config entry."""
    coordinator = EagleDataCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
