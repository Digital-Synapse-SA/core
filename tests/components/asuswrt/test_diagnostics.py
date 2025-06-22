"""Tests for the diagnostics data provided by the AsusWRT integration."""

from smarthub.components.asuswrt.const import DOMAIN
from smarthub.components.asuswrt.diagnostics import TO_REDACT
from smarthub.components.device_tracker import CONF_CONSIDER_HOME
from smarthub.components.diagnostics import async_redact_data
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from .common import CONFIG_DATA_TELNET, ROUTER_MAC_ADDR

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    connect_legacy,
) -> None:
    """Test diagnostics."""
    mock_config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=CONFIG_DATA_TELNET,
        options={CONF_CONSIDER_HOME: 60},
        unique_id=ROUTER_MAC_ADDR,
    )
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_config_entry.state is ConfigEntryState.LOADED

    entry_dict = async_redact_data(mock_config_entry.as_dict(), TO_REDACT)

    result = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    )

    assert result["entry"] == entry_dict | {"discovery_keys": {}}
