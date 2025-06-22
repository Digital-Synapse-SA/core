"""Diagnostics support for Plugwise."""

from __future__ import annotations

from typing import Any

from smarthub.core import SmartHub

from .coordinator import PlugwiseConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: PlugwiseConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return coordinator.data
