"""Diagnostics platform for IronOS integration."""

from __future__ import annotations

from typing import Any

from smarthub.const import CONF_ADDRESS
from smarthub.core import SmartHub

from . import IronOSConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub, config_entry: IronOSConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "config_entry_data": {
            CONF_ADDRESS: config_entry.unique_id,
        },
        "device_info": config_entry.runtime_data.live_data.device_info,
        "live_data": config_entry.runtime_data.live_data.data,
        "settings_data": config_entry.runtime_data.settings.data,
    }
