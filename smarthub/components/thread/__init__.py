"""The Thread integration."""

from __future__ import annotations

from smarthub.config_entries import SOURCE_IMPORT, ConfigEntry
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType

from .const import DOMAIN
from .dataset_store import (
    DatasetEntry,
    async_add_dataset,
    async_get_dataset,
    async_get_preferred_dataset,
)
from .websocket_api import async_setup as async_setup_ws_api

__all__ = [
    "DOMAIN",
    "DatasetEntry",
    "async_add_dataset",
    "async_get_dataset",
    "async_get_preferred_dataset",
]

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the Thread integration."""
    if not hass.config_entries.async_entries(DOMAIN):
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": SOURCE_IMPORT}
            )
        )
    async_setup_ws_api(hass)
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up a config entry."""

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
