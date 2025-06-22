"""Test pushbullet integration."""

from unittest.mock import patch

from pushbullet import InvalidKeyError, PushbulletError

from smarthub.components.pushbullet.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.const import EVENT_HOMEASSISTANT_START
from smarthub.core import SmartHub

from . import MOCK_CONFIG

from tests.common import MockConfigEntry


async def test_async_setup_entry_success(
    hass: SmartHub, requests_mock_fixture
) -> None:
    """Test pushbullet successful setup."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED

    with patch(
        "smarthub.components.pushbullet.api.PushBulletNotificationProvider.start"
    ) as mock_start:
        hass.bus.async_fire(EVENT_HOMEASSISTANT_START)
        await hass.async_block_till_done()
        mock_start.assert_called_once()


async def test_setup_entry_failed_invalid_key(hass: SmartHub) -> None:
    """Test pushbullet failed setup due to invalid key."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    with patch(
        "smarthub.components.pushbullet.PushBullet",
        side_effect=InvalidKeyError,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_ERROR


async def test_setup_entry_failed_conn_error(hass: SmartHub) -> None:
    """Test pushbullet failed setup due to conn error."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    with patch(
        "smarthub.components.pushbullet.PushBullet",
        side_effect=PushbulletError,
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_async_unload_entry(hass: SmartHub, requests_mock_fixture) -> None:
    """Test pushbullet unload entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED
