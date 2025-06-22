"""Support to control a Salda Smarty XP/XV ventilation unit."""

from smarthub.const import Platform
from smarthub.core import SmartHub

from .coordinator import SmartyConfigEntry, SmartyCoordinator

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.FAN,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: SmartHub, entry: SmartyConfigEntry) -> bool:
    """Set up the Smarty environment from a config entry."""

    coordinator = SmartyCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: SmartyConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
