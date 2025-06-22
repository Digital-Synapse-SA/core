"""The simplepush component."""

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv, discovery
from smarthub.helpers.typing import ConfigType

from .const import DATA_HASS_CONFIG, DOMAIN

PLATFORMS = [Platform.NOTIFY]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the simplepush component."""

    hass.data[DATA_HASS_CONFIG] = config
    return True


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up simplepush from a config entry."""

    hass.async_create_task(
        discovery.async_load_platform(
            hass,
            Platform.NOTIFY,
            DOMAIN,
            dict(entry.data),
            hass.data[DATA_HASS_CONFIG],
        )
    )

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
