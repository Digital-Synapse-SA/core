"""Diagnostics support for Environment Canada."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import CONF_LATITUDE, CONF_LONGITUDE
from smarthub.core import SmartHub

from .coordinator import ECConfigEntry

TO_REDACT = {CONF_LATITUDE, CONF_LONGITUDE}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, config_entry: ECConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "config_entry_data": async_redact_data(dict(config_entry.data), TO_REDACT),
        "weather_data": dict(
            config_entry.runtime_data.weather_coordinator.ec_data.conditions
        ),
    }
