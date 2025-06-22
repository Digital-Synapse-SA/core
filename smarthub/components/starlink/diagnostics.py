"""Fetches diagnostic data for Starlink systems."""

from dataclasses import asdict
from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.core import SmartHub

from .coordinator import StarlinkConfigEntry

TO_REDACT = {"id", "latitude", "longitude", "altitude"}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, config_entry: StarlinkConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for Starlink config entries."""
    return async_redact_data(asdict(config_entry.runtime_data.data), TO_REDACT)
