"""The PVOutput integration."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .const import DOMAIN, PLATFORMS
from .coordinator import PVOutputDataUpdateCoordinator


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up PVOutput from a config entry."""
    coordinator = PVOutputDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload PVOutput config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        del hass.data[DOMAIN][entry.entry_id]
    return unload_ok
