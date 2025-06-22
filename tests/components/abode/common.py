"""Common methods used across tests for Abode."""

from unittest.mock import patch

from smarthub.components.abode import DOMAIN
from smarthub.components.abode.const import CONF_POLLING
from smarthub.const import CONF_PASSWORD, CONF_USERNAME
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from tests.common import MockConfigEntry


async def setup_platform(hass: SmartHub, platform: str) -> MockConfigEntry:
    """Set up the Abode platform."""
    mock_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "user@email.com",
            CONF_PASSWORD: "password",
            CONF_POLLING: False,
        },
    )
    mock_entry.add_to_hass(hass)

    with (
        patch("smarthub.components.abode.PLATFORMS", [platform]),
        patch("jaraco.abode.event_controller.sio"),
    ):
        assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    return mock_entry
