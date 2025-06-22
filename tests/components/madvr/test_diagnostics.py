"""Test madVR diagnostics."""

from unittest.mock import AsyncMock, patch

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from smarthub.const import Platform
from smarthub.core import SmartHub

from . import setup_integration
from .conftest import get_update_callback

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


@pytest.mark.parametrize(
    ("positive_payload"),
    [
        {"is_on": True},
    ],
)
async def test_entry_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    mock_madvr_client: AsyncMock,
    snapshot: SnapshotAssertion,
    positive_payload: dict,
) -> None:
    """Test config entry diagnostics."""
    with patch("smarthub.components.madvr.PLATFORMS", [Platform.SENSOR]):
        await setup_integration(hass, mock_config_entry)

    update_callback = get_update_callback(mock_madvr_client)

    # Add data to test storing diagnostic data
    update_callback(positive_payload)
    await hass.async_block_till_done()

    result = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    )

    assert result == snapshot(exclude=props("created_at", "modified_at"))
