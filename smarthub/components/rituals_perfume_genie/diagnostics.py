"""Diagnostics support for Rituals Perfume Genie."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .const import DOMAIN
from .coordinator import RitualsDataUpdateCoordinator

TO_REDACT = {
    "hublot",
    "hash",
}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinators: dict[str, RitualsDataUpdateCoordinator] = hass.data[DOMAIN][
        entry.entry_id
    ]
    return {
        "diffusers": [
            async_redact_data(coordinator.diffuser.data, TO_REDACT)
            for coordinator in coordinators.values()
        ]
    }
