"""Diagnostics support for Tile."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_UUID
from smarthub.core import SmartHub

from .coordinator import TileConfigEntry

CONF_ALTITUDE = "altitude"

TO_REDACT = {
    CONF_ALTITUDE,
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_UUID,
}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: TileConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinators = entry.runtime_data.values()

    return async_redact_data(
        {"tiles": [coordinator.tile.as_dict() for coordinator in coordinators]},
        TO_REDACT,
    )
