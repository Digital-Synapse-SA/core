"""Tests for the Meater sensors."""

from unittest.mock import AsyncMock, patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry, snapshot_platform


@pytest.mark.freeze_time("2023-10-21")
async def test_entities(
    hass: SmartHub,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_meater_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the sensor entities."""
    with patch("smarthub.components.meater.PLATFORMS", [Platform.SENSOR]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
