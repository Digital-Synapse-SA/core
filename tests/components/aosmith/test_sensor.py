"""Tests for the sensor platform of the A. O. Smith integration."""

from collections.abc import AsyncGenerator
from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


@pytest.fixture(autouse=True)
async def platforms() -> AsyncGenerator[None]:
    """Return the platforms to be loaded for this test."""
    with patch("smarthub.components.aosmith.PLATFORMS", [Platform.SENSOR]):
        yield


async def test_state(
    hass: SmartHub,
    init_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test the state of the sensor entities."""
    await snapshot_platform(hass, entity_registry, snapshot, init_integration.entry_id)
