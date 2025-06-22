"""Diagnostics platform for Russound RIO."""

from typing import Any

from smarthub.core import SmartHub

from . import RussoundConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: RussoundConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for the provided config entry."""
    return entry.runtime_data.state
