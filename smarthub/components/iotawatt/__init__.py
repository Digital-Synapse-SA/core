"""The iotawatt integration."""

from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import IotawattConfigEntry, IotawattUpdater

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: SmartHub, entry: IotawattConfigEntry) -> bool:
    """Set up iotawatt from a config entry."""
    coordinator = IotawattUpdater(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: IotawattConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
