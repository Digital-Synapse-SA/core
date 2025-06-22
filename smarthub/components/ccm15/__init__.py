"""The Midea ccm15 AC Controller integration."""

from __future__ import annotations

from smarthub.const import CONF_HOST, CONF_PORT, Platform
from smarthub.core import SmartHub

from .coordinator import CCM15ConfigEntry, CCM15Coordinator

PLATFORMS: list[Platform] = [Platform.CLIMATE]


async def async_setup_entry(hass: SmartHub, entry: CCM15ConfigEntry) -> bool:
    """Set up Midea ccm15 AC Controller from a config entry."""

    coordinator = CCM15Coordinator(
        hass,
        entry,
        entry.data[CONF_HOST],
        entry.data[CONF_PORT],
    )
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: CCM15ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
