"""The Israel Rail component."""

import logging

from israelrailapi import TrainSchedule

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryNotReady

from .const import CONF_DESTINATION, CONF_START, DOMAIN
from .coordinator import IsraelRailConfigEntry, IsraelRailDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: SmartHub, entry: IsraelRailConfigEntry) -> bool:
    """Set up Israel rail from a config entry."""
    config = entry.data

    start = config[CONF_START]
    destination = config[CONF_DESTINATION]

    train_schedule = TrainSchedule()

    try:
        await hass.async_add_executor_job(train_schedule.query, start, destination)
    except Exception as e:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="request_timeout",
            translation_placeholders={
                "config_title": entry.title,
                "error": str(e),
            },
        ) from e

    israel_rail_coordinator = IsraelRailDataUpdateCoordinator(
        hass, entry, train_schedule, start, destination
    )
    await israel_rail_coordinator.async_config_entry_first_refresh()
    entry.runtime_data = israel_rail_coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: IsraelRailConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
