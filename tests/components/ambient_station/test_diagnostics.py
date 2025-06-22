"""Test Ambient PWS diagnostics."""

from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from smarthub.components.ambient_station import AmbientStationConfigEntry
from smarthub.core import SmartHub

from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_entry_diagnostics(
    hass: SmartHub,
    config_entry: AmbientStationConfigEntry,
    hass_client: ClientSessionGenerator,
    data_station,
    setup_config_entry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    ambient = config_entry.runtime_data
    ambient.stations = data_station
    assert await get_diagnostics_for_config_entry(
        hass, hass_client, config_entry
    ) == snapshot(exclude=props("created_at", "modified_at"))
