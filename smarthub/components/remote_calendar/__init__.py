"""The Remote Calendar integration."""

import logging

from smarthub.const import Platform
from smarthub.core import SmartHub

from .const import DOMAIN
from .coordinator import RemoteCalendarConfigEntry, RemoteCalendarDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


PLATFORMS: list[Platform] = [Platform.CALENDAR]


async def async_setup_entry(
    hass: SmartHub, entry: RemoteCalendarConfigEntry
) -> bool:
    """Set up Remote Calendar from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    coordinator = RemoteCalendarDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: SmartHub, entry: RemoteCalendarConfigEntry
) -> bool:
    """Handle unload of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
