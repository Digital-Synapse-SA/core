"""Diagnostics support for TwenteMilieu."""

from __future__ import annotations

from typing import Any

from smarthub.core import SmartHub

from .coordinator import TwenteMilieuConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: TwenteMilieuConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        f"WasteType.{waste_type.name}": [
            waste_date.isoformat() for waste_date in waste_dates
        ]
        for waste_type, waste_dates in entry.runtime_data.data.items()
    }
