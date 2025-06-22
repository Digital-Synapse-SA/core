"""Alexa Devices integration."""

from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import AmazonConfigEntry, AmazonDevicesCoordinator

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.NOTIFY,
    Platform.SWITCH,
]


async def async_setup_entry(hass: SmartHub, entry: AmazonConfigEntry) -> bool:
    """Set up Alexa Devices platform."""

    coordinator = AmazonDevicesCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: AmazonConfigEntry) -> bool:
    """Unload a config entry."""
    await entry.runtime_data.api.close()
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
