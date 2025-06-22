"""Diagnostics for the Cookidoo integration."""

from dataclasses import asdict
from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import CONF_PASSWORD
from smarthub.core import SmartHub

from .coordinator import CookidooConfigEntry

TO_REDACT = [
    CONF_PASSWORD,
]


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: CookidooConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "data": asdict(entry.runtime_data.data),
        "user": asdict(entry.runtime_data.user),
    }
