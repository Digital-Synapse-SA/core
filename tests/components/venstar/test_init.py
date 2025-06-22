"""Tests of the initialization of the venstar integration."""

from unittest.mock import patch

from smarthub.components.venstar.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.const import CONF_HOST, CONF_SSL
from smarthub.core import SmartHub

from . import VenstarColorTouchMock

from tests.common import MockConfigEntry

TEST_HOST = "venstartest.localdomain"


async def test_setup_entry(hass: SmartHub) -> None:
    """Validate that setup entry also configure the client."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: TEST_HOST,
            CONF_SSL: False,
        },
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "smarthub.components.venstar.VenstarColorTouch._request",
            new=VenstarColorTouchMock._request,
        ),
        patch(
            "smarthub.components.venstar.VenstarColorTouch.update_sensors",
            new=VenstarColorTouchMock.update_sensors,
        ),
        patch(
            "smarthub.components.venstar.VenstarColorTouch.update_info",
            new=VenstarColorTouchMock.update_info,
        ),
        patch(
            "smarthub.components.venstar.VenstarColorTouch.update_alerts",
            new=VenstarColorTouchMock.update_alerts,
        ),
        patch(
            "smarthub.components.venstar.VenstarColorTouch.get_runtimes",
            new=VenstarColorTouchMock.get_runtimes,
        ),
        patch(
            "smarthub.components.venstar.coordinator.VENSTAR_SLEEP",
            new=0,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    await hass.config_entries.async_unload(config_entry.entry_id)

    assert config_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_entry_exception(hass: SmartHub) -> None:
    """Validate that setup entry also configure the client."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: TEST_HOST,
            CONF_SSL: False,
        },
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "smarthub.components.venstar.VenstarColorTouch._request",
            new=VenstarColorTouchMock._request,
        ),
        patch(
            "smarthub.components.venstar.VenstarColorTouch.update_sensors",
            new=VenstarColorTouchMock.update_sensors,
        ),
        patch(
            "smarthub.components.venstar.VenstarColorTouch.update_info",
            new=VenstarColorTouchMock.broken_update_info,
        ),
        patch(
            "smarthub.components.venstar.VenstarColorTouch.update_alerts",
            new=VenstarColorTouchMock.update_alerts,
        ),
        patch(
            "smarthub.components.venstar.VenstarColorTouch.get_runtimes",
            new=VenstarColorTouchMock.get_runtimes,
        ),
    ):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_RETRY
