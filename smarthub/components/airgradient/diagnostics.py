"""Diagnostics support for Airgradient."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from smarthub.core import SmartHub

from . import AirGradientConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: AirGradientConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return asdict(entry.runtime_data.data)
