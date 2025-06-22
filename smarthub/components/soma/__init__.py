"""Support for Soma Smartshades."""

from __future__ import annotations

from api.soma_api import SomaApi
import voluptuous as vol

from smarthub import config_entries
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_HOST, CONF_PORT, Platform
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType

from .const import API, DEVICES, DOMAIN, HOST, PORT

CONFIG_SCHEMA = vol.Schema(
    vol.All(
        cv.deprecated(DOMAIN),
        {
            DOMAIN: vol.Schema(
                {vol.Required(CONF_HOST): cv.string, vol.Required(CONF_PORT): cv.string}
            )
        },
    ),
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = [Platform.COVER, Platform.SENSOR]


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the Soma component."""
    if DOMAIN not in config:
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            data=config[DOMAIN],
            context={"source": config_entries.SOURCE_IMPORT},
        )
    )

    return True


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Set up Soma from a config entry."""
    hass.data[DOMAIN] = {}
    api = await hass.async_add_executor_job(SomaApi, entry.data[HOST], entry.data[PORT])
    devices = await hass.async_add_executor_job(api.list_devices)
    hass.data[DOMAIN] = {API: api, DEVICES: devices["shades"]}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: SmartHub, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
