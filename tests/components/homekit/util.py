"""Test util for the homekit integration."""

from unittest.mock import patch

from smarthub.components.homekit.const import DOMAIN
from smarthub.const import CONF_NAME, CONF_PORT
from smarthub.core import SmartHub

from tests.common import MockConfigEntry

PATH_HOMEKIT = "smarthub.components.homekit"


async def async_init_integration(hass: SmartHub) -> MockConfigEntry:
    """Set up the homekit integration in SmartHub."""

    with patch(f"{PATH_HOMEKIT}.HomeKit.async_start"):
        entry = MockConfigEntry(
            domain=DOMAIN, data={CONF_NAME: "mock_name", CONF_PORT: 12345}
        )
        entry.add_to_hass(hass)
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        return entry


async def async_init_entry(hass: SmartHub, entry: MockConfigEntry):
    """Set up the homekit integration in SmartHub."""

    with patch(f"{PATH_HOMEKIT}.HomeKit.async_start"):
        entry.add_to_hass(hass)
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        return entry
