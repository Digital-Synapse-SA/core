"""Test ViCare diagnostics."""

from unittest.mock import MagicMock

from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from smarthub.core import SmartHub

from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    mock_vicare_gas_boiler: MagicMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""
    diag = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_vicare_gas_boiler
    )

    assert diag == snapshot(exclude=props("created_at", "modified_at"))
