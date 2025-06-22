"""Test fixtures for IoTaWatt."""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from smarthub.components.iotawatt.const import DOMAIN
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


@pytest.fixture
def entry(hass: SmartHub) -> MockConfigEntry:
    """Mock config entry added to HA."""
    entry = MockConfigEntry(domain=DOMAIN, data={"host": "1.2.3.4"})
    entry.add_to_hass(hass)
    return entry


@pytest.fixture
def mock_iotawatt(entry: MockConfigEntry) -> Generator[MagicMock]:
    """Mock iotawatt."""
    with patch("smarthub.components.iotawatt.coordinator.Iotawatt") as mock:
        instance = mock.return_value
        instance.connect = AsyncMock(return_value=True)
        instance.update = AsyncMock()
        instance.getSensors.return_value = {"sensors": {}}
        yield instance
