"""Tests for the Habitica switch platform."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

from aiohttp import ClientError
import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)
from smarthub.config_entries import ConfigEntryState
from smarthub.const import ATTR_ENTITY_ID, Platform
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers import entity_registry as er

from .conftest import ERROR_BAD_REQUEST, ERROR_TOO_MANY_REQUESTS

from tests.common import MockConfigEntry, snapshot_platform


@pytest.fixture(autouse=True)
def switch_only() -> Generator[None]:
    """Enable only the switch platform."""
    with patch(
        "smarthub.components.habitica.PLATFORMS",
        [Platform.SWITCH],
    ):
        yield


@pytest.mark.usefixtures("habitica")
async def test_switch(
    hass: SmartHub,
    config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test switch entities."""

    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.parametrize(
    ("service_call"),
    [
        SERVICE_TURN_ON,
        SERVICE_TURN_OFF,
        SERVICE_TOGGLE,
    ],
)
async def test_turn_on_off_toggle(
    hass: SmartHub,
    config_entry: MockConfigEntry,
    service_call: str,
    habitica: AsyncMock,
) -> None:
    """Test switch turn on/off, toggle method."""

    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    await hass.services.async_call(
        SWITCH_DOMAIN,
        service_call,
        {ATTR_ENTITY_ID: "switch.test_user_rest_in_the_inn"},
        blocking=True,
    )

    habitica.toggle_sleep.assert_awaited_once()


@pytest.mark.parametrize(
    ("service_call"),
    [
        SERVICE_TURN_ON,
        SERVICE_TURN_OFF,
        SERVICE_TOGGLE,
    ],
)
@pytest.mark.parametrize(
    ("raise_exception", "expected_exception"),
    [
        (ERROR_TOO_MANY_REQUESTS, SmartHubError),
        (ERROR_BAD_REQUEST, SmartHubError),
        (ClientError, SmartHubError),
    ],
)
async def test_turn_on_off_toggle_exceptions(
    hass: SmartHub,
    config_entry: MockConfigEntry,
    service_call: str,
    habitica: AsyncMock,
    raise_exception: Exception,
    expected_exception: Exception,
) -> None:
    """Test switch turn on/off, toggle method."""

    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    habitica.toggle_sleep.side_effect = raise_exception

    with pytest.raises(expected_exception=expected_exception):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            service_call,
            {ATTR_ENTITY_ID: "switch.test_user_rest_in_the_inn"},
            blocking=True,
        )
