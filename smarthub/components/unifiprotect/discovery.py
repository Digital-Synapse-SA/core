"""The unifiprotect integration discovery."""

from __future__ import annotations

from dataclasses import asdict
from datetime import timedelta
import logging
from typing import Any

from unifi_discovery import AIOUnifiScanner, UnifiDevice, UnifiService

from smarthub import config_entries
from smarthub.core import SmartHub, callback
from smarthub.helpers import discovery_flow
from smarthub.helpers.event import async_track_time_interval

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DISCOVERY = "discovery"
DISCOVERY_INTERVAL = timedelta(minutes=60)


@callback
def async_start_discovery(hass: SmartHub) -> None:
    """Start discovery."""
    domain_data = hass.data.setdefault(DOMAIN, {})
    if DISCOVERY in domain_data:
        return
    domain_data[DISCOVERY] = True

    async def _async_discovery() -> None:
        async_trigger_discovery(hass, await async_discover_devices())

    @callback
    def _async_start_background_discovery(*_: Any) -> None:
        """Run discovery in the background."""
        hass.async_create_background_task(_async_discovery(), "unifiprotect-discovery")

    # Do not block startup since discovery takes 31s or more
    _async_start_background_discovery()
    async_track_time_interval(
        hass,
        _async_start_background_discovery,
        DISCOVERY_INTERVAL,
        cancel_on_shutdown=True,
    )


async def async_discover_devices() -> list[UnifiDevice]:
    """Discover devices."""
    scanner = AIOUnifiScanner()
    devices = await scanner.async_scan()
    _LOGGER.debug("Found devices: %s", devices)
    return devices


@callback
def async_trigger_discovery(
    hass: SmartHub,
    discovered_devices: list[UnifiDevice],
) -> None:
    """Trigger config flows for discovered devices."""
    for device in discovered_devices:
        if device.services[UnifiService.Protect] and device.hw_addr:
            discovery_flow.async_create_flow(
                hass,
                DOMAIN,
                context={"source": config_entries.SOURCE_INTEGRATION_DISCOVERY},
                data=asdict(device),
            )
