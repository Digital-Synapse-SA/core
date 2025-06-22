"""Diagnostics support for Google Generative AI Conversation."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_API_KEY
from smarthub.core import SmartHub

TO_REDACT = {CONF_API_KEY}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {
            "title": entry.title,
            "data": entry.data,
            "options": entry.options,
        },
        TO_REDACT,
    )
