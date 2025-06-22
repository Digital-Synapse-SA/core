"""Diagnostics support for Eagle."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .const import CONF_CLOUD_ID, CONF_INSTALL_CODE, DOMAIN
from .coordinator import EagleDataCoordinator

TO_REDACT = {CONF_CLOUD_ID, CONF_INSTALL_CODE}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, config_entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: EagleDataCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    return {
        "config_entry": async_redact_data(config_entry.as_dict(), TO_REDACT),
        "data": coordinator.data,
    }
