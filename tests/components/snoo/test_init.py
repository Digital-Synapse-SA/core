"""Test init for Snoo."""

from unittest.mock import AsyncMock

from python_snoo.exceptions import SnooAuthException

from smarthub.components.snoo import SnooDeviceError
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from . import async_init_integration


async def test_async_setup_entry(hass: SmartHub, bypass_api: AsyncMock) -> None:
    """Test a successful setup entry."""
    entry = await async_init_integration(hass)
    assert len(hass.states.async_all("sensor")) == 2
    assert entry.state == ConfigEntryState.LOADED


async def test_cannot_auth(hass: SmartHub, bypass_api: AsyncMock) -> None:
    """Test that we are put into retry when we fail to auth."""
    bypass_api.authorize.side_effect = SnooAuthException
    entry = await async_init_integration(hass)
    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_failed_devices(hass: SmartHub, bypass_api: AsyncMock) -> None:
    """Test that we are put into retry when we fail to get devices."""
    bypass_api.get_devices.side_effect = SnooDeviceError
    entry = await async_init_integration(hass)
    assert entry.state is ConfigEntryState.SETUP_RETRY
