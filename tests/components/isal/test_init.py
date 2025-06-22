"""Test the Intelligent Storage Acceleration setup."""

from smarthub.components.isal import DOMAIN
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component


async def test_setup(hass: SmartHub) -> None:
    """Ensure we can setup."""
    assert await async_setup_component(hass, DOMAIN, {})
