"""Support for LiteJet diagnostics."""

from typing import Any

from pylitejet import LiteJet

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for LiteJet config entry."""
    system: LiteJet = hass.data[DOMAIN]
    return {
        "model": system.model_name,
        "loads": list(system.loads()),
        "button_switches": list(system.button_switches()),
        "scenes": list(system.scenes()),
        "connected": system.connected,
    }
