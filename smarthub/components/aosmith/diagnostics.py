"""Diagnostics support for A. O. Smith."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.core import SmartHub

from .coordinator import AOSmithConfigEntry

TO_REDACT = {
    "address",
    "city",
    "contactId",
    "dsn",
    "email",
    "firstName",
    "heaterSsid",
    "id",
    "lastName",
    "phone",
    "postalCode",
    "registeredOwner",
    "serial",
    "ssid",
    "state",
}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, config_entry: AOSmithConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = config_entry.runtime_data

    all_device_info = await data.client.get_all_device_info()
    return async_redact_data(all_device_info, TO_REDACT)
