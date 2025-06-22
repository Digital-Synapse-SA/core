"""Test the Aquacell init module."""

from __future__ import annotations

from unittest.mock import AsyncMock

from syrupy.assertion import SnapshotAssertion

from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry, snapshot_platform


async def test_sensors(
    hass: SmartHub,
    mock_aquacell_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the creation of Aquacell sensors."""
    await setup_integration(hass, mock_config_entry)
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
