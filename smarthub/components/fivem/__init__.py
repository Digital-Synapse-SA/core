"""The FiveM integration."""

from __future__ import annotations

import logging

from fivem import FiveMServerOfflineError

from smarthub.const import CONF_HOST, CONF_PORT, Platform
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryNotReady

from .coordinator import FiveMConfigEntry, FiveMDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: SmartHub, entry: FiveMConfigEntry) -> bool:
    """Set up FiveM from a config entry."""
    _LOGGER.debug(
        "Create FiveM server instance for '%s:%s'",
        entry.data[CONF_HOST],
        entry.data[CONF_PORT],
    )

    coordinator = FiveMDataUpdateCoordinator(hass, entry)

    try:
        await coordinator.initialize()
    except FiveMServerOfflineError as err:
        raise ConfigEntryNotReady from err

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: FiveMConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
