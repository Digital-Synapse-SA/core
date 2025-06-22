"""The html5 component."""

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import discovery

from .const import DOMAIN


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up HTML5 from a config entry."""
    await discovery.async_load_platform(
        hass, Platform.NOTIFY, DOMAIN, dict(entry.data), {}
    )
    return True
