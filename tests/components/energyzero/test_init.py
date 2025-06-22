"""Tests for the EnergyZero integration."""

from unittest.mock import MagicMock, patch

from energyzero import EnergyZeroConnectionError
import pytest

from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


@pytest.mark.usefixtures("mock_energyzero")
async def test_load_unload_config_entry(
    hass: SmartHub, mock_config_entry: MockConfigEntry
) -> None:
    """Test the EnergyZero configuration entry loading/unloading."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


@patch(
    "smarthub.components.energyzero.coordinator.EnergyZero._request",
    side_effect=EnergyZeroConnectionError,
)
async def test_config_flow_entry_not_ready(
    mock_request: MagicMock,
    hass: SmartHub,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the EnergyZero configuration entry not ready."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_request.call_count == 1
    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
