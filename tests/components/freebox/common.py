"""Common methods used across tests for Freebox."""

from unittest.mock import patch

from smarthub.components.freebox.const import DOMAIN
from smarthub.const import CONF_HOST, CONF_PORT
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from .const import MOCK_HOST, MOCK_PORT

from tests.common import MockConfigEntry


async def setup_platform(hass: SmartHub, platform: str) -> MockConfigEntry:
    """Set up the Freebox platform."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_HOST: MOCK_HOST, CONF_PORT: MOCK_PORT},
        unique_id=MOCK_HOST,
    )
    mock_entry.add_to_hass(hass)

    with patch("smarthub.components.freebox.PLATFORMS", [platform]):
        assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    return mock_entry
