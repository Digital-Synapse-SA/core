"""Config flow for Zerproc."""

import logging

import pyzerproc

from smarthub.core import SmartHub
from smarthub.helpers import config_entry_flow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def _async_has_devices(hass: SmartHub) -> bool:
    """Return if there are devices that can be discovered."""
    try:
        devices = await pyzerproc.discover()
        return len(devices) > 0
    except pyzerproc.ZerprocException:
        _LOGGER.exception("Unable to discover nearby Zerproc devices")
        return False


config_entry_flow.register_discovery_flow(DOMAIN, "Zerproc", _async_has_devices)
