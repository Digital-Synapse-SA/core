"""Test Météo France weather entity."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with patch("smarthub.components.meteo_france.PLATFORMS", [Platform.WEATHER]):
        yield


async def test_weather(
    hass: SmartHub,
    config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the weather entity."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)
