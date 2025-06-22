"""Test Jellyfin diagnostics."""

from syrupy.assertion import SnapshotAssertion

from smarthub.core import SmartHub

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_diagnostics(
    hass: SmartHub,
    init_integration: MockConfigEntry,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a config entry."""
    data = await get_diagnostics_for_config_entry(hass, hass_client, init_integration)

    assert data["entry"]["data"]["client_device_id"] == init_integration.entry_id
    data["entry"]["data"]["client_device_id"] = "entry-id"

    assert data == snapshot
