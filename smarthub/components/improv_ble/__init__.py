"""The Improv BLE integration."""

from __future__ import annotations

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up improv_ble from a config entry."""
    raise NotImplementedError
