"""The notify_events component."""

import voluptuous as vol

from smarthub.const import CONF_TOKEN, Platform
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv, discovery
from smarthub.helpers.typing import ConfigType

from .const import DOMAIN

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({vol.Required(CONF_TOKEN): cv.string})}, extra=vol.ALLOW_EXTRA
)


def setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the notify_events component."""

    hass.data[DOMAIN] = config[DOMAIN]
    discovery.load_platform(hass, Platform.NOTIFY, DOMAIN, {}, config)
    return True
