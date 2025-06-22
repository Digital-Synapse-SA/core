"""Test the Tessie binary sensor platform."""

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from .common import assert_entities, setup_platform


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_binary_sensors(
    hass: SmartHub, snapshot: SnapshotAssertion, entity_registry: er.EntityRegistry
) -> None:
    """Tests that the binary sensor entities are correct."""

    entry = await setup_platform(hass, [Platform.BINARY_SENSOR])

    assert_entities(hass, entry.entry_id, entity_registry, snapshot)
