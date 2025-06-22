"""Diagnostics support for IMGW-PIB."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from smarthub.core import SmartHub

from .coordinator import ImgwPibConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ImgwPibConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data.coordinator

    return {
        "config_entry_data": entry.as_dict(),
        "hydrological_data": asdict(coordinator.data),
    }
