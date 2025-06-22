"""Diagnostics support for SamsungTV."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import CONF_TOKEN
from smarthub.core import SmartHub

from .const import CONF_SESSION_ID
from .coordinator import SamsungTVConfigEntry

TO_REDACT = {CONF_TOKEN, CONF_SESSION_ID}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: SamsungTVConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "device_info": await coordinator.bridge.async_device_info(),
    }
