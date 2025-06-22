"""Diagnostics support for Tankerkoenig."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import (
    CONF_API_KEY,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_UNIQUE_ID,
)
from smarthub.core import SmartHub

from .coordinator import TankerkoenigConfigEntry

TO_REDACT = {CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, CONF_UNIQUE_ID}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: TankerkoenigConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "data": {
            station_id: asdict(price_info)
            for station_id, price_info in coordinator.data.items()
        },
    }
