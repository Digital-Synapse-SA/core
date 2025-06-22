"""Diagnostics support for nexia."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.core import SmartHub

from .const import CONF_BRAND
from .types import NexiaConfigEntry

TO_REDACT = {
    "dealer_contact_info",
}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: NexiaConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    nexia_home = coordinator.nexia_home

    return {
        "entry": {
            "title": entry.title,
            "brand": entry.data.get(CONF_BRAND),
        },
        "automations": async_redact_data(nexia_home.automations_json, TO_REDACT),
        "devices": async_redact_data(nexia_home.devices_json, TO_REDACT),
    }
