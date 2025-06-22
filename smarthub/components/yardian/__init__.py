"""The Yardian integration."""

from __future__ import annotations

from pyyardian import AsyncYardianClient

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_ACCESS_TOKEN, CONF_HOST, Platform
from smarthub.core import SmartHub
from smarthub.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .coordinator import YardianUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SWITCH]


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up Yardian from a config entry."""

    host = entry.data[CONF_HOST]
    access_token = entry.data[CONF_ACCESS_TOKEN]

    controller = AsyncYardianClient(async_get_clientsession(hass), host, access_token)
    coordinator = YardianUpdateCoordinator(hass, entry, controller)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)

    return unload_ok
