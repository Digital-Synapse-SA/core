"""Test cases and object for the Switcher integration tests."""

from smarthub.components.switcher_kis.const import DOMAIN
from smarthub.const import CONF_TOKEN, CONF_USERNAME
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def init_integration(
    hass: SmartHub, username: str | None = None, token: str | None = None
) -> MockConfigEntry:
    """Set up the Switcher integration in SmartHub."""
    data = {}
    if username is not None:
        data[CONF_USERNAME] = username
    if token is not None:
        data[CONF_TOKEN] = token

    entry = MockConfigEntry(domain=DOMAIN, data=data, unique_id=DOMAIN)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    return entry
