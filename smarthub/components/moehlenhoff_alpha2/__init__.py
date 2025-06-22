"""Support for the Moehlenhoff Alpha2."""

from __future__ import annotations

from moehlenhoff_alpha2 import Alpha2Base

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_HOST, Platform
from smarthub.core import SmartHub

from .const import DOMAIN
from .coordinator import Alpha2BaseCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.BUTTON, Platform.CLIMATE, Platform.SENSOR]


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    base = Alpha2Base(entry.data[CONF_HOST])
    coordinator = Alpha2BaseCoordinator(hass, entry, base)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: SmartHub, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
