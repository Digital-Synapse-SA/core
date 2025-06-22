"""Diagnostics support for Schlage."""

from __future__ import annotations

from typing import Any

from smarthub.core import SmartHub

from .coordinator import SchlageConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub,
    config_entry: SchlageConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = config_entry.runtime_data
    # NOTE: Schlage diagnostics are already redacted.
    return {
        "locks": [ld.lock.get_diagnostics() for ld in coordinator.data.locks.values()]
    }
