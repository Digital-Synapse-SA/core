"""The tests for the persistent notification component."""

import pytest

from smarthub.components import persistent_notification as pn
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component


@pytest.fixture(autouse=True)
async def setup_integration(hass: SmartHub) -> None:
    """Set up persistent notification integration."""
    assert await async_setup_component(hass, pn.DOMAIN, {})
