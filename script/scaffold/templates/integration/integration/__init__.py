"""The NEW_NAME integration."""

from __future__ import annotations

import voluptuous as vol

from smarthub.core import SmartHub
from smarthub.helpers.typing import ConfigType

from .const import DOMAIN

CONFIG_SCHEMA = vol.Schema({vol.Optional(DOMAIN): {}}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Set up the NEW_NAME integration."""
    return True
