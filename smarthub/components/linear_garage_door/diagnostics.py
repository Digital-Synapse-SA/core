"""Diagnostics support for Linear Garage Door."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_EMAIL, CONF_PASSWORD
from smarthub.core import SmartHub

from .const import DOMAIN
from .coordinator import LinearUpdateCoordinator

TO_REDACT = {CONF_PASSWORD, CONF_EMAIL}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: LinearUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "coordinator_data": {
            device_id: asdict(device_data)
            for device_id, device_data in coordinator.data.items()
        },
    }
