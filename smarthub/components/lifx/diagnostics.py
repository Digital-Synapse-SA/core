"""Diagnostics support for LIFX."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_HOST, CONF_IP_ADDRESS, CONF_MAC
from smarthub.core import SmartHub

from .const import CONF_LABEL, DOMAIN
from .coordinator import LIFXUpdateCoordinator

TO_REDACT = [CONF_LABEL, CONF_HOST, CONF_IP_ADDRESS, CONF_MAC]


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a LIFX config entry."""
    coordinator: LIFXUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    return {
        "entry": {
            "title": entry.title,
            "data": async_redact_data(dict(entry.data), TO_REDACT),
        },
        "data": async_redact_data(await coordinator.diagnostics(), TO_REDACT),
    }
