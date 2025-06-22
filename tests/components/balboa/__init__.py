"""Test the Balboa Spa Client integration."""

from __future__ import annotations

from unittest.mock import MagicMock

from smarthub.components.balboa.const import CONF_SYNC_TIME, DOMAIN
from smarthub.const import CONF_HOST
from smarthub.core import SmartHub, State

from tests.common import MockConfigEntry

TEST_HOST = "balboatest.localdomain"


async def init_integration(hass: SmartHub) -> MockConfigEntry:
    """Mock integration setup."""
    entry = MockConfigEntry(
        domain=DOMAIN, data={CONF_HOST: TEST_HOST}, options={CONF_SYNC_TIME: True}
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


async def client_update(hass: SmartHub, client: MagicMock, entity: str) -> State:
    """Update the client."""
    client.emit("")
    await hass.async_block_till_done()
    assert (state := hass.states.get(entity)) is not None
    return state
