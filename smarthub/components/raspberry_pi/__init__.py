"""The Raspberry Pi integration."""

from __future__ import annotations

from smarthub.components.hassio import get_os_info
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryNotReady
from smarthub.helpers.hassio import is_hassio


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up a Raspberry Pi config entry."""
    if not is_hassio(hass):
        # Not running under supervisor, SmartHub may have been migrated
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        return False

    if (os_info := get_os_info(hass)) is None:
        # The hassio integration has not yet fetched data from the supervisor
        raise ConfigEntryNotReady

    board: str | None
    if (board := os_info.get("board")) is None or not board.startswith("rpi"):
        # Not running on a Raspberry Pi, SmartHub may have been migrated
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        return False

    await hass.config_entries.flow.async_init(
        "rpi_power", context={"source": "onboarding"}
    )

    return True
