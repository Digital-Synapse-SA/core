"""The test for the Yale Smart Alarm binary sensor platform."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


@pytest.mark.parametrize(
    "load_platforms",
    [[Platform.BINARY_SENSOR]],
)
async def test_binary_sensor(
    hass: SmartHub,
    load_config_entry: tuple[MockConfigEntry, Mock],
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the Yale Smart Alarm binary sensor."""
    entry = load_config_entry[0]
    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
