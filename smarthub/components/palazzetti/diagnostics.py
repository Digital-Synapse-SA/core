"""Provides diagnostics for Palazzetti."""

from __future__ import annotations

from typing import Any

from smarthub.core import SmartHub

from .coordinator import PalazzettiConfigEntry


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: PalazzettiConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    client = entry.runtime_data.client

    return {
        "api_data": client.to_dict(redact=True),
    }
