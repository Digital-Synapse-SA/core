"""The venstar component."""

from __future__ import annotations

from venstarcolortouch import VenstarColorTouch

from smarthub.config_entries import ConfigEntry
from smarthub.const import (
    CONF_HOST,
    CONF_PASSWORD,
    CONF_PIN,
    CONF_SSL,
    CONF_USERNAME,
    Platform,
)
from smarthub.core import SmartHub

from .const import DOMAIN, VENSTAR_TIMEOUT
from .coordinator import VenstarDataUpdateCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.CLIMATE, Platform.SENSOR]


async def async_setup_entry(hass: SmartHub, config_entry: ConfigEntry) -> bool:
    """Set up the Venstar thermostat."""
    username = config_entry.data.get(CONF_USERNAME)
    password = config_entry.data.get(CONF_PASSWORD)
    pin = config_entry.data.get(CONF_PIN)
    host = config_entry.data[CONF_HOST]
    timeout = VENSTAR_TIMEOUT
    protocol = "https" if config_entry.data[CONF_SSL] else "http"

    client = VenstarColorTouch(
        addr=host,
        timeout=timeout,
        user=username,
        password=password,
        pin=pin,
        proto=protocol,
    )

    venstar_data_coordinator = VenstarDataUpdateCoordinator(
        hass,
        config_entry,
        venstar_connection=client,
    )
    await venstar_data_coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = venstar_data_coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, config_entry: ConfigEntry) -> bool:
    """Unload the config and platforms."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, PLATFORMS
    )
    if unload_ok:
        hass.data[DOMAIN].pop(config_entry.entry_id)
    return unload_ok
