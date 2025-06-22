"""Diagnostics support for Notion."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_EMAIL, CONF_UNIQUE_ID, CONF_USERNAME
from smarthub.core import SmartHub

from .const import CONF_REFRESH_TOKEN, CONF_USER_UUID, DOMAIN
from .coordinator import NotionDataUpdateCoordinator

CONF_DEVICE_KEY = "device_key"
CONF_HARDWARE_ID = "hardware_id"
CONF_LAST_BRIDGE_HARDWARE_ID = "last_bridge_hardware_id"
CONF_TITLE = "title"
CONF_USER_ID = "user_id"

TO_REDACT = {
    CONF_DEVICE_KEY,
    CONF_EMAIL,
    CONF_HARDWARE_ID,
    CONF_LAST_BRIDGE_HARDWARE_ID,
    CONF_REFRESH_TOKEN,
    # Config entry title and unique ID may contain sensitive data:
    CONF_TITLE,
    CONF_UNIQUE_ID,
    CONF_USERNAME,
    CONF_USER_ID,
    CONF_USER_UUID,
}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: NotionDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    return async_redact_data(
        {
            "entry": entry.as_dict(),
            "data": coordinator.data.asdict(),
        },
        TO_REDACT,
    )
