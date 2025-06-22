"""Test the One-Time Password (OTP) init."""

from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def test_entry_setup_unload(
    hass: SmartHub, otp_config_entry: MockConfigEntry
) -> None:
    """Test integration setup and unload."""

    otp_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(otp_config_entry.entry_id)
    await hass.async_block_till_done()

    assert otp_config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(otp_config_entry.entry_id)
    await hass.async_block_till_done()

    assert otp_config_entry.state is ConfigEntryState.NOT_LOADED
