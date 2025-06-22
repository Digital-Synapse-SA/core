"""The SmartHub Green integration."""

from __future__ import annotations

from smarthub.components.hassio import get_os_info
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryNotReady
from smarthub.helpers.hassio import is_hassio


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up a SmartHub Green config entry."""
    if not is_hassio(hass):
        # Not running under supervisor, SmartHub may have been migrated
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        return False

    if (os_info := get_os_info(hass)) is None:
        # The hassio integration has not yet fetched data from the supervisor
        raise ConfigEntryNotReady

    board: str | None
    if (board := os_info.get("board")) is None or board != "green":
        # Not running on a SmartHub Green, SmartHub may have been migrated
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        return False

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
