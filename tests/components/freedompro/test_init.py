"""Freedompro component tests."""

import logging
from unittest.mock import patch

from smarthub.components.freedompro.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from tests.common import MockConfigEntry

LOGGER = logging.getLogger(__name__)

ENTITY_ID = f"{DOMAIN}.fake_name"


async def test_async_setup_entry(
    hass: SmartHub, init_integration: MockConfigEntry
) -> None:
    """Test a successful setup entry."""
    entry = init_integration
    assert entry is not None
    state = hass.states
    assert state is not None


async def test_config_not_ready(hass: SmartHub) -> None:
    """Test for setup failure if connection to Freedompro is missing."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Feedompro",
        unique_id="0123456",
        data={
            "api_key": "gdhsksjdhcncjdkdjndjdkdmndjdjdkd",
        },
    )

    with patch(
        "smarthub.components.freedompro.coordinator.get_list",
        return_value={
            "state": False,
        },
    ):
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_unload_entry(
    hass: SmartHub, init_integration: MockConfigEntry
) -> None:
    """Test successful unload of entry."""
    entry = init_integration

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.NOT_LOADED
