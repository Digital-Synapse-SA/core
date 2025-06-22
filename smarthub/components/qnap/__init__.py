"""The qnap component."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub

from .const import DOMAIN
from .coordinator import QnapCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(hass: SmartHub, config_entry: ConfigEntry) -> bool:
    """Set the config entry up."""
    hass.data.setdefault(DOMAIN, {})
    coordinator = QnapCoordinator(hass, config_entry)
    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][config_entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    ):
        hass.data[DOMAIN].pop(config_entry.entry_id)
    return unload_ok
