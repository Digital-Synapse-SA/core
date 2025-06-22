"""Tests for the melissa component."""

from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

VALID_CONFIG = {"melissa": {"username": "********", "password": "********"}}


async def setup_integration(hass: SmartHub) -> None:
    """Set up the melissa integration in SmartHub."""
    assert await async_setup_component(hass, "melissa", VALID_CONFIG)
    await hass.async_block_till_done()
