"""The trafikverket_ferry component."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .const import PLATFORMS
from .coordinator import TVDataUpdateCoordinator

TVFerryConfigEntry = ConfigEntry[TVDataUpdateCoordinator]


async def async_setup_entry(hass: SmartHub, entry: TVFerryConfigEntry) -> bool:
    """Set up Trafikverket Ferry from a config entry."""

    coordinator = TVDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: TVFerryConfigEntry) -> bool:
    """Unload Trafikverket Ferry config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
