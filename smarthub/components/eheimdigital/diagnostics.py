"""Diagnostics for the EHEIM Digital integration."""

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.core import SmartHub

from .coordinator import EheimDigitalConfigEntry

TO_REDACT = {"emailAddr", "usrName"}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: EheimDigitalConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {"entry": entry.as_dict(), "data": entry.runtime_data.data}, TO_REDACT
    )
