"""group conftest."""

import pytest

from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from tests.components.light.conftest import mock_light_profiles  # noqa: F401


@pytest.fixture(autouse=True)
async def setup_smarthub(hass: SmartHub):
    """Set up the smarthub integration."""
    await async_setup_component(hass, "smarthub", {})
