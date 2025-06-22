"""Tests for the nuki binary sensors."""

from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import init_integration

from tests.common import snapshot_platform


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_binary_sensors(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test binary sensors."""
    with patch("smarthub.components.nuki.PLATFORMS", [Platform.BINARY_SENSOR]):
        entry = await init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
