"""Test for event platform of the Bring! integration."""

from collections.abc import Generator
from unittest.mock import patch

from freezegun.api import freeze_time
import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.config_entries import ConfigEntryState
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform


@pytest.fixture(autouse=True)
def event_only() -> Generator[None]:
    """Enable only the event platform."""
    with patch(
        "smarthub.components.bring.PLATFORMS",
        [Platform.EVENT],
    ):
        yield


@pytest.mark.usefixtures("mock_bring_client")
@freeze_time("2025-01-01T03:30:00.000Z")
async def test_setup(
    hass: SmartHub,
    bring_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Snapshot test states of event platform."""

    bring_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(bring_config_entry.entry_id)
    await hass.async_block_till_done()

    assert bring_config_entry.state is ConfigEntryState.LOADED

    await snapshot_platform(
        hass, entity_registry, snapshot, bring_config_entry.entry_id
    )
