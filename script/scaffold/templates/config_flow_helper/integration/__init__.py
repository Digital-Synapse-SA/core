"""The NEW_NAME integration."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up NEW_NAME from a config entry."""
    # TODO Optionally store an object for your platforms to access
    # entry.runtime_data = ...

    # TODO Optionally validate config entry options before setting up platform

    await hass.config_entries.async_forward_entry_setups(entry, (Platform.SENSOR,))

    # TODO Remove if the integration does not have an options flow
    entry.async_on_unload(entry.add_update_listener(config_entry_update_listener))

    return True


# TODO Remove if the integration does not have an options flow
async def config_entry_update_listener(hass: SmartHub, entry: ConfigEntry) -> None:
    """Update listener, called when the config entry options are changed."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, (Platform.SENSOR,))
