"""The HVV integration."""

from smarthub.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from smarthub.core import SmartHub
from smarthub.helpers import aiohttp_client

from .hub import GTIHub, HVVConfigEntry

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass: SmartHub, entry: HVVConfigEntry) -> bool:
    """Set up HVV from a config entry."""

    hub = GTIHub(
        entry.data[CONF_HOST],
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD],
        aiohttp_client.async_get_clientsession(hass),
    )

    entry.runtime_data = hub

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: HVVConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
