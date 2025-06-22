"""Tests for the local_ip component."""

from __future__ import annotations

from smarthub.components.local_ip.const import DOMAIN
from smarthub.components.network import MDNS_TARGET_IP, async_get_source_ip
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def test_basic_setup(hass: SmartHub) -> None:
    """Test component setup creates entry from config."""
    entry = MockConfigEntry(domain=DOMAIN, data={})
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED

    local_ip = await async_get_source_ip(hass, target_ip=MDNS_TARGET_IP)
    state = hass.states.get(f"sensor.{DOMAIN}")
    assert state
    assert state.state == local_ip

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED
