"""Diagnostics support for Jewish Calendar integration."""

from dataclasses import asdict
from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import CONF_LATITUDE, CONF_LONGITUDE
from smarthub.core import SmartHub

from .const import CONF_ALTITUDE
from .entity import JewishCalendarConfigEntry

TO_REDACT = [
    CONF_ALTITUDE,
    CONF_LATITUDE,
    CONF_LONGITUDE,
]


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: JewishCalendarConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "entry_data": async_redact_data(entry.data, TO_REDACT),
        "data": async_redact_data(asdict(entry.runtime_data), TO_REDACT),
    }
