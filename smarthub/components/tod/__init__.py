"""The Times of the Day integration."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up Times of the Day from a config entry."""
    await hass.config_entries.async_forward_entry_setups(
        entry, (Platform.BINARY_SENSOR,)
    )

    entry.async_on_unload(entry.add_update_listener(config_entry_update_listener))

    return True


async def config_entry_update_listener(hass: SmartHub, entry: ConfigEntry) -> None:
    """Update listener, called when the config entry options are changed."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(
        entry, (Platform.BINARY_SENSOR,)
    )
