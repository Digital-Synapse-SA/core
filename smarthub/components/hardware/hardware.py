"""The Hardware integration."""

from __future__ import annotations

from smarthub.core import SmartHub, callback
from smarthub.exceptions import SmartHubError
from smarthub.helpers.integration_platform import (
    async_process_integration_platforms,
)

from .const import DATA_HARDWARE, DOMAIN
from .models import HardwareProtocol


async def async_process_hardware_platforms(
    hass: SmartHub,
) -> None:
    """Start processing hardware platforms."""
    await async_process_integration_platforms(
        hass, DOMAIN, _register_hardware_platform, wait_for_platforms=True
    )


@callback
def _register_hardware_platform(
    hass: SmartHub, integration_domain: str, platform: HardwareProtocol
) -> None:
    """Register a hardware platform."""
    if integration_domain == DOMAIN:
        return
    if not hasattr(platform, "async_info"):
        raise SmartHubError(f"Invalid hardware platform {platform}")
    hass.data[DATA_HARDWARE].hardware_platform[integration_domain] = platform
