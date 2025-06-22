"""Diagnostics support for Sensor.Community."""

from __future__ import annotations

from typing import Any

from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_LATITUDE, CONF_LONGITUDE
from smarthub.core import SmartHub
from smarthub.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_SENSOR_ID, DOMAIN

TO_REDACT = {
    CONF_LATITUDE,
    CONF_LONGITUDE,
    CONF_SENSOR_ID,
}


async def async_get_config_entry_diagnostics(
    hass: SmartHub, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: DataUpdateCoordinator[dict[str, Any]] = hass.data[DOMAIN][
        entry.entry_id
    ]
    return async_redact_data(coordinator.data, TO_REDACT)
