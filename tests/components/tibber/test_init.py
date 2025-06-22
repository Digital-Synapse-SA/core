"""Test loading of the Tibber config entry."""

from unittest.mock import MagicMock

from smarthub.components.recorder import Recorder
from smarthub.components.tibber import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub


async def test_entry_unload(
    recorder_mock: Recorder, hass: SmartHub, mock_tibber_setup: MagicMock
) -> None:
    """Test unloading the entry."""
    entry = hass.config_entries.async_entry_for_domain_unique_id(DOMAIN, "tibber")
    assert entry.state == ConfigEntryState.LOADED

    await hass.config_entries.async_unload(entry.entry_id)
    mock_tibber_setup.rt_disconnect.assert_called_once()
    await hass.async_block_till_done(wait_background_tasks=True)
    assert entry.state == ConfigEntryState.NOT_LOADED
