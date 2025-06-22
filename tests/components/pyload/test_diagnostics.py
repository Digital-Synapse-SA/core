"""Tests for pyLoad diagnostics."""

from unittest.mock import AsyncMock

from syrupy.assertion import SnapshotAssertion

from smarthub.core import SmartHub

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    config_entry: MockConfigEntry,
    mock_pyloadapi: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, config_entry)
        == snapshot
    )
