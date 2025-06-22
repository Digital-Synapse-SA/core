"""demo conftest."""

from unittest.mock import patch

import pytest

from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from tests.components.light.conftest import mock_light_profiles  # noqa: F401


@pytest.fixture(autouse=True, name="stub_blueprint_populate")
def stub_blueprint_populate_autouse(stub_blueprint_populate: None) -> None:
    """Stub copying the blueprints to the config folder."""


@pytest.fixture(autouse=True)
async def setup_smarthub(hass: SmartHub):
    """Set up the smarthub integration."""
    await async_setup_component(hass, "smarthub", {})


@pytest.fixture
def disable_platforms(hass: SmartHub) -> None:
    """Disable platforms to speed up tests."""
    with (
        patch(
            "smarthub.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
            [],
        ),
        patch(
            "smarthub.components.demo.COMPONENTS_WITH_DEMO_PLATFORM",
            [],
        ),
    ):
        yield
