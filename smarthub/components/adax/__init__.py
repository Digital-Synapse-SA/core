"""The Adax integration."""

from __future__ import annotations

from smarthub.const import Platform
from smarthub.core import SmartHub

from .const import CONNECTION_TYPE, LOCAL
from .coordinator import AdaxCloudCoordinator, AdaxConfigEntry, AdaxLocalCoordinator

PLATFORMS = [Platform.CLIMATE, Platform.SENSOR]


async def async_setup_entry(hass: SmartHub, entry: AdaxConfigEntry) -> bool:
    """Set up Adax from a config entry."""
    if entry.data.get(CONNECTION_TYPE) == LOCAL:
        local_coordinator = AdaxLocalCoordinator(hass, entry)
        entry.runtime_data = local_coordinator
    else:
        cloud_coordinator = AdaxCloudCoordinator(hass, entry)
        entry.runtime_data = cloud_coordinator

    await entry.runtime_data.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: AdaxConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_migrate_entry(
    hass: SmartHub, config_entry: AdaxConfigEntry
) -> bool:
    """Migrate old entry."""
    # convert title and unique_id to string
    if config_entry.version == 1:
        if isinstance(config_entry.unique_id, int):
            hass.config_entries.async_update_entry(  # type: ignore[unreachable]
                config_entry,
                unique_id=str(config_entry.unique_id),
                title=str(config_entry.title),
            )

    return True
