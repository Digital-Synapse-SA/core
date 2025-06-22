"""Diagnostics support for Open-Meteo."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import CONF_LATITUDE, CONF_LONGITUDE
from smarthub.core import SmartHub

from .coordinator import OpenMeteoConfigEntry

TO_REDACT = {
    CONF_LATITUDE,
    CONF_LONGITUDE,
}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: OpenMeteoConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return async_redact_data(coordinator.data.to_dict(), TO_REDACT)
