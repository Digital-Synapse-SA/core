"""Diagnostics support for Workday."""

from __future__ import annotations

from typing import Any

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "config_entry": entry,
    }
