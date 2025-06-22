"""Diagnostics support for Devialet."""

from __future__ import annotations

from typing import Any

from smarthub.core import SmartHub

from .coordinator import DevialetConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: DevialetConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return await entry.runtime_data.client.async_get_diagnostics()
