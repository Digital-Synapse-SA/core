"""Support for Melissa climate."""

from melissa import AsyncMelissa
import voluptuous as vol

from smarthub.const import CONF_PASSWORD, CONF_USERNAME, Platform
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.discovery import async_load_platform
from smarthub.helpers.typing import ConfigType

DOMAIN = "melissa"
DATA_MELISSA = "MELISSA"


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the Melissa Climate component."""
    conf = config[DOMAIN]
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)
    api = AsyncMelissa(username=username, password=password)
    await api.async_connect()
    hass.data[DATA_MELISSA] = api

    hass.async_create_task(
        async_load_platform(hass, Platform.CLIMATE, DOMAIN, {}, config)
    )
    return True
