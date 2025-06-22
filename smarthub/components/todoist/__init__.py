"""The todoist integration."""

import datetime
import logging

from todoist_api_python.api_async import TodoistAPIAsync

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_TOKEN, Platform
from smarthub.core import SmartHub

from .const import DOMAIN
from .coordinator import TodoistCoordinator

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = datetime.timedelta(minutes=1)


PLATFORMS: list[Platform] = [Platform.CALENDAR, Platform.TODO]


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up todoist from a config entry."""

    token = entry.data[CONF_TOKEN]
    api = TodoistAPIAsync(token)
    coordinator = TodoistCoordinator(hass, _LOGGER, entry, SCAN_INTERVAL, api, token)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
