"""Define fixtures available for all Acmeda tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest

from smarthub.components.acmeda.const import DOMAIN
from smarthub.const import CONF_HOST
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


@pytest.fixture
def mock_config_entry(hass: SmartHub) -> MockConfigEntry:
    """Return the default mocked config entry."""
    mock_config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: "127.0.0.1"},
    )
    mock_config_entry.add_to_hass(hass)
    return mock_config_entry


@pytest.fixture
def mock_hub_run() -> Generator[AsyncMock]:
    """Mock the hub run method."""
    with patch("smarthub.components.acmeda.hub.aiopulse.Hub.run") as mock_run:
        yield mock_run
