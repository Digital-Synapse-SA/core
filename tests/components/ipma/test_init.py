"""Test the IPMA integration."""

from unittest.mock import patch

from pyipma import IPMAException

from smarthub.components.ipma.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_MODE
from smarthub.core import SmartHub

from .test_weather import MockLocation

from tests.common import MockConfigEntry


async def test_async_setup_raises_entry_not_ready(hass: SmartHub) -> None:
    """Test that it throws ConfigEntryNotReady when exception occurs during setup."""

    with patch(
        "pyipma.location.Location.get", side_effect=IPMAException("API unavailable")
    ):
        config_entry = MockConfigEntry(
            domain=DOMAIN,
            title="Home",
            data={CONF_LATITUDE: 0, CONF_LONGITUDE: 0, CONF_MODE: "daily"},
        )

        config_entry.add_to_hass(hass)

        await hass.config_entries.async_setup(config_entry.entry_id)

        assert config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_unload_config_entry(hass: SmartHub) -> None:
    """Test entry unloading."""

    with patch(
        "pyipma.location.Location.get",
        return_value=MockLocation(),
    ):
        config_entry = MockConfigEntry(
            domain="ipma",
            data={CONF_LATITUDE: 0, CONF_LONGITUDE: 0, CONF_MODE: "daily"},
        )
        config_entry.add_to_hass(hass)

        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.LOADED

        await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()

        assert config_entry.state is ConfigEntryState.NOT_LOADED
