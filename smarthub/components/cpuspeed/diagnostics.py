"""Diagnostics support for CPU Speed."""

from __future__ import annotations

from typing import Any

from cpuinfo import cpuinfo

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    info: dict[str, Any] = cpuinfo.get_cpu_info()
    return info
