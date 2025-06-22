"""Tests for the ccm15 component."""

import pytest

from smarthub.components.ccm15.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.const import CONF_HOST, CONF_PORT
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


@pytest.mark.usefixtures("ccm15_device")
async def test_load_unload(hass: SmartHub) -> None:
    """Test options flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="1.1.1.1",
        data={
            CONF_HOST: "1.1.1.1",
            CONF_PORT: 80,
        },
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
