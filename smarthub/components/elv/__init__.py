"""The Elv integration."""

import voluptuous as vol

from smarthub.const import CONF_DEVICE, Platform
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv, discovery
from smarthub.helpers.typing import ConfigType

DOMAIN = "elv"

DEFAULT_DEVICE = "/dev/ttyUSB0"

ELV_PLATFORMS = [Platform.SWITCH]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {vol.Optional(CONF_DEVICE, default=DEFAULT_DEVICE): cv.string}
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the PCA switch platform."""

    for platform in ELV_PLATFORMS:
        discovery.load_platform(
            hass, platform, DOMAIN, {"device": config[DOMAIN][CONF_DEVICE]}, config
        )

    return True
