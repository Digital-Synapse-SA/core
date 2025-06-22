"""The isal integration."""

from __future__ import annotations

from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv
from smarthub.helpers.typing import ConfigType

DOMAIN = "isal"

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up up isal.

    This integration is only used so that isal can be an optional
    dep for aiohttp-fast-zlib.
    """
    return True
