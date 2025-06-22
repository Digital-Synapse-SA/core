"""The edl21 component."""

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: SmartHub, config_entry: ConfigEntry) -> bool:
    """Set up EDL21 integration from a config entry."""
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
