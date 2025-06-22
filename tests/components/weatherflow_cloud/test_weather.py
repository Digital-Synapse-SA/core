"""Tests for the WeatherFlow Cloud weather platform."""

from unittest.mock import AsyncMock, patch

from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry, snapshot_platform


async def test_weather(
    hass: SmartHub,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    mock_api: AsyncMock,
) -> None:
    """Test all entities."""
    with patch(
        "smarthub.components.weatherflow_cloud.PLATFORMS", [Platform.WEATHER]
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
