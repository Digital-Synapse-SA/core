"""Test cases for the Webmin sensors."""

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from .conftest import async_init_integration

from tests.common import snapshot_platform


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensor(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the sensor entities and states."""

    entry = await async_init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
