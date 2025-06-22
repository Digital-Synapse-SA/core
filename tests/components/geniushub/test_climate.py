"""Tests for the Geniushub climate platform."""

from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry, snapshot_platform


@pytest.mark.usefixtures("mock_geniushub_cloud")
async def test_cloud_all_sensors(
    hass: SmartHub,
    mock_cloud_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the creation of the Genius Hub climate entities."""
    with patch("smarthub.components.geniushub.PLATFORMS", [Platform.CLIMATE]):
        await setup_integration(hass, mock_cloud_config_entry)

    await snapshot_platform(
        hass, entity_registry, snapshot, mock_cloud_config_entry.entry_id
    )
