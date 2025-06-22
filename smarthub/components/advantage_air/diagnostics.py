"""Provides diagnostics for Advantage Air."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.core import SmartHub

from . import AdvantageAirDataConfigEntry

TO_REDACT = [
    "dealerPhoneNumber",
    "latitude",
    "logoPIN",
    "longitude",
    "postCode",
    "rid",
    "deviceNames",
    "deviceIds",
    "deviceIdsV2",
    "backupId",
]


async def async_get_config_entry_diagnostics(
    hass: SmartHub, config_entry: AdvantageAirDataConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = config_entry.runtime_data.coordinator.data

    # Return only the relevant children
    return {
        "aircons": data.get("aircons"),
        "myLights": data.get("myLights"),
        "myThings": data.get("myThings"),
        "system": async_redact_data(data["system"], TO_REDACT),
    }
