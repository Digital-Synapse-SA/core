"""Test init."""

from unittest.mock import MagicMock

import httpx

from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from . import INPUT_SENSOR

from tests.common import MockConfigEntry


async def test_setup_unload(
    hass: SmartHub, mock_iotawatt: MagicMock, entry: MockConfigEntry
) -> None:
    """Test we can setup and unload an entry."""
    mock_iotawatt.getSensors.return_value["sensors"]["my_sensor_key"] = INPUT_SENSOR
    assert await async_setup_component(hass, "iotawatt", {})
    await hass.async_block_till_done()
    assert await hass.config_entries.async_unload(entry.entry_id)


async def test_setup_connection_failed(
    hass: SmartHub, mock_iotawatt: MagicMock, entry: MockConfigEntry
) -> None:
    """Test connection error during startup."""
    mock_iotawatt.connect.side_effect = httpx.ConnectError("")
    assert await async_setup_component(hass, "iotawatt", {})
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_setup_auth_failed(
    hass: SmartHub, mock_iotawatt: MagicMock, entry: MockConfigEntry
) -> None:
    """Test auth error during startup."""
    mock_iotawatt.connect.return_value = False
    assert await async_setup_component(hass, "iotawatt", {})
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY
