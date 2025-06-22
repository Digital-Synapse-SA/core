"""Test the SFR Box setup process."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from sfrbox_api.exceptions import SFRBoxAuthenticationError, SFRBoxError

from smarthub.components.sfr_box.const import DOMAIN
from smarthub.config_entries import ConfigEntry, ConfigEntryState
from smarthub.core import SmartHub


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with patch("smarthub.components.sfr_box.PLATFORMS", []):
        yield


@pytest.mark.usefixtures("system_get_info", "dsl_get_info", "wan_get_info")
async def test_setup_unload_entry(
    hass: SmartHub, config_entry: ConfigEntry
) -> None:
    """Test entry setup and unload."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert config_entry.state is ConfigEntryState.LOADED

    # Unload the entry and verify that the data has been removed
    await hass.config_entries.async_unload(config_entry.entry_id)
    await hass.async_block_till_done()
    assert config_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_entry_exception(
    hass: SmartHub, config_entry: ConfigEntry
) -> None:
    """Test ConfigEntryNotReady when API raises an exception during entry setup."""
    with patch(
        "smarthub.components.sfr_box.coordinator.SFRBox.system_get_info",
        side_effect=SFRBoxError,
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert config_entry.state is ConfigEntryState.SETUP_RETRY
    assert not hass.data.get(DOMAIN)


async def test_setup_entry_auth_exception(
    hass: SmartHub, config_entry_with_auth: ConfigEntry
) -> None:
    """Test ConfigEntryNotReady when API raises an exception during authentication."""
    with patch(
        "smarthub.components.sfr_box.coordinator.SFRBox.authenticate",
        side_effect=SFRBoxError,
    ):
        await hass.config_entries.async_setup(config_entry_with_auth.entry_id)
        await hass.async_block_till_done()

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert config_entry_with_auth.state is ConfigEntryState.SETUP_RETRY
    assert not hass.data.get(DOMAIN)


async def test_setup_entry_invalid_auth(
    hass: SmartHub, config_entry_with_auth: ConfigEntry
) -> None:
    """Test ConfigEntryAuthFailed when API raises an exception during authentication."""
    with patch(
        "smarthub.components.sfr_box.coordinator.SFRBox.authenticate",
        side_effect=SFRBoxAuthenticationError,
    ):
        await hass.config_entries.async_setup(config_entry_with_auth.entry_id)
        await hass.async_block_till_done()

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert config_entry_with_auth.state is ConfigEntryState.SETUP_ERROR
    assert not hass.data.get(DOMAIN)
