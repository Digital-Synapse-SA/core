"""Tests for the easyEnergy integration."""

from unittest.mock import MagicMock, patch

from easyenergy import EasyEnergyConnectionError

from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def test_load_unload_config_entry(
    hass: SmartHub, mock_config_entry: MockConfigEntry, mock_easyenergy: MagicMock
) -> None:
    """Test the easyEnergy configuration entry loading/unloading."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


@patch(
    "smarthub.components.easyenergy.coordinator.EasyEnergy._request",
    side_effect=EasyEnergyConnectionError,
)
async def test_config_flow_entry_not_ready(
    mock_request: MagicMock,
    hass: SmartHub,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the easyEnergy configuration entry not ready."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_request.call_count == 1
    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY
