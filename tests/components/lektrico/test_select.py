"""Tests for the Lektrico select platform."""

from unittest.mock import AsyncMock, patch

from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry, snapshot_platform


async def test_all_entities(
    hass: SmartHub,
    snapshot: SnapshotAssertion,
    mock_device: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch.multiple(
        "smarthub.components.lektrico",
        CHARGERS_PLATFORMS=[Platform.SELECT],
        LB_DEVICES_PLATFORMS=[Platform.SELECT],
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
