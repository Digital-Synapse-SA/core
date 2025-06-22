"""Test Solarlog diagnostics."""

from unittest.mock import AsyncMock

from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from smarthub.const import Platform
from smarthub.core import SmartHub

from . import setup_platform

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_entry_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    mock_solarlog_connector: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    await setup_platform(hass, mock_config_entry, [Platform.SENSOR])

    result = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    )

    assert result == snapshot(exclude=props("created_at", "modified_at"))
