"""Diagnostics support for IMAP."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.const import CONF_PASSWORD, CONF_USERNAME
from smarthub.core import SmartHub, callback

from . import ImapConfigEntry

REDACT_CONFIG = {CONF_PASSWORD, CONF_USERNAME}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ImapConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return _async_get_diagnostics(hass, entry)


@callback
def _async_get_diagnostics(
    hass: SmartHub,
    entry: ImapConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    redacted_config = async_redact_data(entry.data, REDACT_CONFIG)
    coordinator = entry.runtime_data

    return {
        "config": redacted_config,
        "event": coordinator.diagnostics_data,
    }
