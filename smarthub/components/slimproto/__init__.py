"""SlimProto Player integration."""

from __future__ import annotations

from aioslimproto import SlimServer

from smarthub.config_entries import ConfigEntry
from smarthub.const import EVENT_HOMEASSISTANT_STOP, Platform
from smarthub.core import Event, SmartHub
from smarthub.helpers import device_registry as dr

from .const import DOMAIN

PLATFORMS = [Platform.MEDIA_PLAYER]


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    slimserver = SlimServer()
    await slimserver.start()

    hass.data[DOMAIN] = slimserver

    # initialize platform(s)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # setup event listeners
    async def on_hass_stop(event: Event) -> None:
        """Handle incoming stop event from SmartHub."""
        await slimserver.stop()

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, on_hass_stop)
    )

    return True


async def async_remove_config_entry_device(
    hass: SmartHub, config_entry: ConfigEntry, device_entry: dr.DeviceEntry
) -> bool:
    """Remove a config entry from a device."""
    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_success = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_success:
        await hass.data.pop(DOMAIN).stop()
    return unload_success
