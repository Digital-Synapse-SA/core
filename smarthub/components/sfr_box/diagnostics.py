"""SFR Box diagnostics platform."""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .const import DOMAIN
from .models import DomainData

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

TO_REDACT = {"mac_addr", "serial_number", "ip_addr", "ipv6_addr"}


def _async_redact_data(obj: DataclassInstance | None) -> dict[str, Any] | None:
    if obj is None:
        return None
    return async_redact_data(dataclasses.asdict(obj), TO_REDACT)


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data: DomainData = hass.data[DOMAIN][entry.entry_id]

    return {
        "entry": {
            "title": entry.title,
            "data": dict(entry.data),
        },
        "data": {
            "dsl": _async_redact_data(await data.system.box.dsl_get_info()),
            "ftth": _async_redact_data(await data.system.box.ftth_get_info()),
            "system": _async_redact_data(await data.system.box.system_get_info()),
            "wan": _async_redact_data(await data.system.box.wan_get_info()),
        },
    }
