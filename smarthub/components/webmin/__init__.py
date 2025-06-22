"""The Webmin integration."""

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import WebminUpdateCoordinator

PLATFORMS = [Platform.SENSOR]

type WebminConfigEntry = ConfigEntry[WebminUpdateCoordinator]


async def async_setup_entry(hass: SmartHub, entry: WebminConfigEntry) -> bool:
    """Set up Webmin from a config entry."""

    coordinator = WebminUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    await coordinator.async_setup()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: SmartHub, entry: WebminConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
