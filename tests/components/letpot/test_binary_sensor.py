"""Test binary sensor entities for the LetPot integration."""

from unittest.mock import MagicMock, patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry, snapshot_platform


@pytest.mark.parametrize("device_type", ["LPH63", "LPH31"])
@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_all_entities(
    hass: SmartHub,
    snapshot: SnapshotAssertion,
    mock_client: MagicMock,
    mock_device_client: MagicMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    device_type: str,
) -> None:
    """Test binary sensor entities."""
    with patch("smarthub.components.letpot.PLATFORMS", [Platform.BINARY_SENSOR]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
