"""SmartTub integration."""

from smarthub.const import Platform
from smarthub.core import SmartHub

from .controller import SmartTubConfigEntry, SmartTubController

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    Platform.LIGHT,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: SmartHub, entry: SmartTubConfigEntry) -> bool:
    """Set up a smarttub config entry."""

    controller = SmartTubController(hass)

    if not await controller.async_setup_entry(entry):
        return False

    entry.runtime_data = controller

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: SmartTubConfigEntry) -> bool:
    """Remove a smarttub config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
