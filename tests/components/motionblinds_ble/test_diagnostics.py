"""Test Motionblinds Bluetooth diagnostics."""

from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from smarthub.core import SmartHub

from . import setup_integration

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""

    await setup_integration(hass, mock_config_entry)

    assert await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    ) == snapshot(exclude=props("created_at", "modified_at", "repr"))
