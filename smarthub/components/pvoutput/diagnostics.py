"""Diagnostics support for PVOutput."""

from __future__ import annotations

from typing import Any

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .const import DOMAIN
from .coordinator import PVOutputDataUpdateCoordinator


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: PVOutputDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    return coordinator.data.to_dict()
