"""Diagnostics support for LG webOS TV."""

from __future__ import annotations

from typing import Any

from aiowebostv import WebOsClient

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import CONF_CLIENT_SECRET, CONF_HOST, CONF_UNIQUE_ID
from smarthub.core import SmartHub

from . import WebOsTvConfigEntry

TO_REDACT = {
    CONF_CLIENT_SECRET,
    CONF_UNIQUE_ID,
    CONF_HOST,
    "device_id",
    "deviceUUID",
    "icon",
    "largeIcon",
}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: WebOsTvConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    client: WebOsClient = entry.runtime_data

    client_data = {
        "is_registered": client.is_registered(),
        "is_connected": client.is_connected(),
        "tv_info": client.tv_info.__dict__,
        "tv_state": client.tv_state.__dict__,
    }

    return async_redact_data(
        {
            "entry": entry.as_dict(),
            "client": client_data,
        },
        TO_REDACT,
    )
