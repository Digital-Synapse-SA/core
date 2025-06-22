"""Tests for ntfy diagnostics."""

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.components.ntfy.const import DOMAIN
from smarthub.const import CONF_URL
from smarthub.core import SmartHub

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


@pytest.mark.usefixtures("mock_aiontfy")
async def test_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    config_entry: MockConfigEntry,
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


@pytest.mark.usefixtures("mock_aiontfy")
async def test_diagnostics_redacted_url(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics redacted URL."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        title="mydomain",
        data={
            CONF_URL: "http://mydomain/",
        },
        entry_id="123456789",
        subentries_data=[],
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, config_entry)
        == snapshot
    )
