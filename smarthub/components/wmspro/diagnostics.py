"""Diagnostics support for WMS WebControl pro API integration."""

from __future__ import annotations

from typing import Any

from smarthub.core import SmartHub

from . import WebControlProConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: WebControlProConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return entry.runtime_data.diag()
