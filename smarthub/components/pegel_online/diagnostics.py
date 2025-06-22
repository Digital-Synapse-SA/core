"""Diagnostics support for pegel_online."""

from __future__ import annotations

from typing import Any

from smarthub.core import SmartHub

from .coordinator import PegelOnlineConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: PegelOnlineConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "entry": entry.as_dict(),
        "data": coordinator.data,
    }
