"""Tests for the Sense integration."""

from unittest.mock import patch

from smarthub.components.sense.const import DOMAIN
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from tests.common import MockConfigEntry


async def setup_platform(
    hass: SmartHub, config_entry: MockConfigEntry, platform: Platform
) -> MockConfigEntry:
    """Set up the Sense platform."""
    config_entry.add_to_hass(hass)

    with patch("smarthub.components.sense.PLATFORMS", [platform]):
        assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()

    return config_entry
