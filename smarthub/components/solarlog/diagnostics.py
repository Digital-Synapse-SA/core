"""Provides diagnostics for Solarlog."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import CONF_HOST
from smarthub.core import SmartHub

from .coordinator import SolarlogConfigEntry

TO_REDACT = [
    CONF_HOST,
]


async def async_get_config_entry_diagnostics(
    hass: SmartHub, config_entry: SolarlogConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = config_entry.runtime_data.data

    return {
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT),
        "solarlog_data": data.to_dict(),
    }
