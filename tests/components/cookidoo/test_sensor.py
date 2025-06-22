"""Test for sensor platform of the Cookidoo integration."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.config_entries import ConfigEntryState
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


@pytest.fixture(autouse=True)
def sensor_only() -> Generator[None]:
    """Enable only the sensor platform."""
    with patch(
        "smarthub.components.cookidoo.PLATFORMS",
        [Platform.SENSOR],
    ):
        yield


@pytest.mark.usefixtures("mock_cookidoo_client")
async def test_setup(
    hass: SmartHub,
    cookidoo_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Snapshot test states of sensor platform."""

    cookidoo_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(cookidoo_config_entry.entry_id)
    await hass.async_block_till_done()

    assert cookidoo_config_entry.state is ConfigEntryState.LOADED

    await snapshot_platform(
        hass, entity_registry, snapshot, cookidoo_config_entry.entry_id
    )
