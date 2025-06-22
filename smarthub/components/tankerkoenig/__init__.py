"""Ask tankerkoenig.de for petrol price information."""

from __future__ import annotations

from smarthub.const import Platform
from smarthub.core import SmartHub

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN
from .coordinator import TankerkoenigConfigEntry, TankerkoenigDataUpdateCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(
    hass: SmartHub, entry: TankerkoenigConfigEntry
) -> bool:
    """Set a tankerkoenig configuration entry up."""
    hass.data.setdefault(DOMAIN, {})

    coordinator = TankerkoenigDataUpdateCoordinator(hass, entry, DEFAULT_SCAN_INTERVAL)
    await coordinator.async_setup()
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: SmartHub, entry: TankerkoenigConfigEntry
) -> bool:
    """Unload Tankerkoenig config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_update_listener(
    hass: SmartHub, entry: TankerkoenigConfigEntry
) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
