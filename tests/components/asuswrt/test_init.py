"""Tests for the AsusWrt integration."""

from smarthub.components.asuswrt.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.const import EVENT_HOMEASSISTANT_STOP
from smarthub.core import SmartHub

from .common import CONFIG_DATA_TELNET, ROUTER_MAC_ADDR

from tests.common import MockConfigEntry


async def test_disconnect_on_stop(hass: SmartHub, connect_legacy) -> None:
    """Test we close the connection with the router when SmartHubs stops."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=CONFIG_DATA_TELNET,
        unique_id=ROUTER_MAC_ADDR,
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    hass.bus.async_fire(EVENT_HOMEASSISTANT_STOP)
    await hass.async_block_till_done()

    assert connect_legacy.return_value.connection.disconnect.call_count == 1
    assert config_entry.state is ConfigEntryState.LOADED
