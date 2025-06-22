"""Test Discovergy diagnostics."""

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.core import SmartHub

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


@pytest.mark.usefixtures("setup_integration")
async def test_entry_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    result = await get_diagnostics_for_config_entry(hass, hass_client, config_entry)

    assert result == snapshot
