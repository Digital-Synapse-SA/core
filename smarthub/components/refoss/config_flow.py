"""Config Flow for Refoss integration."""

from __future__ import annotations

from smarthub.core import SmartHub
from smarthub.helpers import config_entry_flow

from .const import _LOGGER, DISCOVERY_TIMEOUT, DOMAIN
from .util import refoss_discovery_server


async def _async_has_devices(hass: SmartHub) -> bool:
    """Return if there are devices that can be discovered."""

    refoss_discovery = await refoss_discovery_server(hass)
    devices = await refoss_discovery.broadcast_msg(wait_for=DISCOVERY_TIMEOUT)
    _LOGGER.debug(
        "Discovered devices: [%s]", ", ".join([info.dev_name for info in devices])
    )
    return len(devices) > 0


config_entry_flow.register_discovery_flow(DOMAIN, "Refoss", _async_has_devices)
