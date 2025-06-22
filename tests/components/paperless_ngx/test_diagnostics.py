"""Tests for Paperless-ngx sensor platform."""

from unittest.mock import AsyncMock

from syrupy.assertion import SnapshotAssertion

from smarthub.core import SmartHub

from . import setup_integration

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_config_entry_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    mock_paperless: AsyncMock,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a device entry."""
    await setup_integration(hass, mock_config_entry)
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry)
        == snapshot
    )
