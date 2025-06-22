"""Diagnostics support for RFXCOM RFXtrx."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

TO_REDACT = {"host"}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
    }
