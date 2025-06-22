"""Support for the LiteJet lighting system."""

import logging

import pylitejet

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_PORT, EVENT_HOMEASSISTANT_STOP
from smarthub.core import Event, SmartHub
from smarthub.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up LiteJet via a config entry."""
    port = entry.data[CONF_PORT]

    try:
        system = await pylitejet.open(port)
    except pylitejet.LiteJetError as exc:
        raise ConfigEntryNotReady from exc

    def handle_connected_changed(connected: bool, reason: str) -> None:
        if connected:
            _LOGGER.debug("Connected")
        else:
            _LOGGER.warning("Disconnected %s", reason)

    system.on_connected_changed(handle_connected_changed)

    async def handle_stop(event: Event) -> None:
        await system.close()

    entry.async_on_unload(
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, handle_stop)
    )

    hass.data[DOMAIN] = system

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a LiteJet config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        await hass.data[DOMAIN].close()
        hass.data.pop(DOMAIN)

    return unload_ok
