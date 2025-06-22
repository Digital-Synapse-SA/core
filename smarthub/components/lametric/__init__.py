"""Support for LaMetric time."""

from smarthub.components import notify as hass_notify
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_NAME, Platform
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv, discovery
from smarthub.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS
from .coordinator import LaMetricDataUpdateCoordinator
from .services import async_setup_services

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the LaMetric integration."""
    async_setup_services(hass)
    hass.data[DOMAIN] = {"hass_config": config}
    return True


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up LaMetric from a config entry."""
    coordinator = LaMetricDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Set up notify platform, no entry support for notify component yet,
    # have to use discovery to load platform.
    hass.async_create_task(
        discovery.async_load_platform(
            hass,
            Platform.NOTIFY,
            DOMAIN,
            {CONF_NAME: coordinator.data.name, "entry_id": entry.entry_id},
            hass.data[DOMAIN]["hass_config"],
        )
    )
    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload LaMetric config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        del hass.data[DOMAIN][entry.entry_id]
        await hass_notify.async_reload(hass, DOMAIN)
    return unload_ok
