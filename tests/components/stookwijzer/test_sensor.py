"""Tests for the Stookwijzer sensor platform."""

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


@pytest.mark.usefixtures("init_integration")
async def test_entities(
    hass: SmartHub,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the Stookwijzer entities."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
