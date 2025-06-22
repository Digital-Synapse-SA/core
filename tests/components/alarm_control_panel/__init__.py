"""The tests for Alarm control panel platforms."""

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub


async def help_async_setup_entry_init(
    hass: SmartHub, config_entry: ConfigEntry
) -> bool:
    """Set up test config entry."""
    await hass.config_entries.async_forward_entry_setups(
        config_entry, [Platform.ALARM_CONTROL_PANEL]
    )
    return True


async def help_async_unload_entry(
    hass: SmartHub, config_entry: ConfigEntry
) -> bool:
    """Unload test config emntry."""
    return await hass.config_entries.async_unload_platforms(
        config_entry, [Platform.ALARM_CONTROL_PANEL]
    )
