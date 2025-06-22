"""Diagnostics support for Verisure."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .const import DOMAIN
from .coordinator import VerisureDataUpdateCoordinator

TO_REDACT = {
    "date",
    "area",
    "deviceArea",
    "name",
    "time",
    "reportTime",
    "userString",
}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: VerisureDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    return async_redact_data(coordinator.data, TO_REDACT)
