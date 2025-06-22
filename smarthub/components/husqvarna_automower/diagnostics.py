"""Diagnostics support for Husqvarna Automower."""

from __future__ import annotations

import logging
from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import CONF_ACCESS_TOKEN
from smarthub.core import SmartHub
from smarthub.helpers.device_registry import DeviceEntry

from . import AutomowerConfigEntry
from .const import DOMAIN

CONF_REFRESH_TOKEN = "refresh_token"
POSITIONS = "positions"

TO_REDACT = {
    CONF_ACCESS_TOKEN,
    CONF_REFRESH_TOKEN,
    POSITIONS,
}
_LOGGER = logging.getLogger(__name__)


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: AutomowerConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(entry.as_dict(), TO_REDACT)


async def async_get_device_diagnostics(
    hass: SmartHub, entry: AutomowerConfigEntry, device: DeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device entry."""
    coordinator = entry.runtime_data
    for identifier in device.identifiers:
        if identifier[0] == DOMAIN:
            if (
                coordinator.data[identifier[1]].system.serial_number
                == device.serial_number
            ):
                mower_id = identifier[1]
    return async_redact_data(coordinator.data[mower_id].to_dict(), TO_REDACT)
