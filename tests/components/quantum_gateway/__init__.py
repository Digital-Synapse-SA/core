"""Tests for the quantum_gateway component."""

from smarthub.components.device_tracker import DOMAIN as DEVICE_TRACKER_DOMAIN
from smarthub.const import CONF_PASSWORD, CONF_PLATFORM
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component


async def setup_platform(hass: SmartHub) -> None:
    """Set up the quantum_gateway integration."""
    result = await async_setup_component(
        hass,
        DEVICE_TRACKER_DOMAIN,
        {
            DEVICE_TRACKER_DOMAIN: {
                CONF_PLATFORM: "quantum_gateway",
                CONF_PASSWORD: "fake_password",
            }
        },
    )
    await hass.async_block_till_done()
    assert result
