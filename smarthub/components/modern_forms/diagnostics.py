"""Diagnostics support for Modern Forms."""

from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_MAC
from smarthub.core import SmartHub

from .const import DOMAIN
from .coordinator import ModernFormsDataUpdateCoordinator

REDACT_CONFIG = {CONF_MAC}
REDACT_DEVICE_INFO = {"mac_address", "owner"}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: ModernFormsDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    if TYPE_CHECKING:
        assert coordinator is not None

    return {
        "config_entry": async_redact_data(entry.as_dict(), REDACT_CONFIG),
        "device": {
            "info": async_redact_data(
                asdict(coordinator.modern_forms.info), REDACT_DEVICE_INFO
            ),
            "status": asdict(coordinator.modern_forms.status),
        },
    }
