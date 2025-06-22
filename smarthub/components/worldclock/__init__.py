"""The worldclock component."""

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .const import PLATFORMS


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up Worldclock from a config entry."""

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload World clock config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def update_listener(hass: SmartHub, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
