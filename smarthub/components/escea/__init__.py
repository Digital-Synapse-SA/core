"""Platform for the Escea fireplace."""

from smarthub.components.climate import DOMAIN as CLIMATE_DOMAIN
from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub

from .discovery import async_start_discovery_service, async_stop_discovery_service

PLATFORMS = [CLIMATE_DOMAIN]


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    await async_start_discovery_service(hass)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload the config entry and stop discovery process."""
    await async_stop_discovery_service(hass)
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
