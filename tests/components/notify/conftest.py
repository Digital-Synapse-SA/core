"""Fixtures for Notify platform tests."""

from collections.abc import Generator

import pytest

from smarthub.config_entries import ConfigFlow
from smarthub.core import SmartHub

from tests.common import mock_config_flow, mock_platform


class MockFlow(ConfigFlow):
    """Test flow."""


@pytest.fixture
def config_flow_fixture(hass: SmartHub) -> Generator[None]:
    """Mock config flow."""
    mock_platform(hass, "test.config_flow")

    with mock_config_flow("test", MockFlow):
        yield
