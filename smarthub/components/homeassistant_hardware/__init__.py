"""The SmartHub Hardware integration."""

from __future__ import annotations

from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType

from .const import DATA_COMPONENT, DOMAIN
from .helpers import HardwareInfoDispatcher

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the component."""

    hass.data[DATA_COMPONENT] = HardwareInfoDispatcher(hass)

    return True
