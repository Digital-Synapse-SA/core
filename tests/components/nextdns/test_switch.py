"""Test switch of NextDNS integration."""

from datetime import timedelta
from unittest.mock import Mock, patch

from aiohttp import ClientError
from aiohttp.client_exceptions import ClientConnectorError
from nextdns import ApiError, InvalidApiKeyError
import pytest
from syrupy.assertion import SnapshotAssertion
from tenacity import RetryError

from smarthub.components.nextdns.const import DOMAIN
from smarthub.components.switch import DOMAIN as SWITCH_DOMAIN
from smarthub.config_entries import SOURCE_REAUTH, ConfigEntryState
from smarthub.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    Platform,
)
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers import entity_registry as er
from smarthub.util.dt import utcnow

from . import init_integration, mock_nextdns

from tests.common import async_fire_time_changed, snapshot_platform


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_switch(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test states of the switches."""
    with patch("smarthub.components.nextdns.PLATFORMS", [Platform.SWITCH]):
        entry = await init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)


async def test_switch_on(hass: SmartHub) -> None:
    """Test the switch can be turned on."""
    await init_integration(hass)

    state = hass.states.get("switch.fake_profile_block_page")
    assert state
    assert state.state == STATE_OFF

    with patch(
        "smarthub.components.nextdns.NextDns.set_setting", return_value=True
    ) as mock_switch_on:
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SERVICE_TURN_ON,
            {ATTR_ENTITY_ID: "switch.fake_profile_block_page"},
            blocking=True,
        )
        await hass.async_block_till_done()

        state = hass.states.get("switch.fake_profile_block_page")
        assert state
        assert state.state == STATE_ON

        mock_switch_on.assert_called_once()


async def test_switch_off(hass: SmartHub) -> None:
    """Test the switch can be turned on."""
    await init_integration(hass)

    state = hass.states.get("switch.fake_profile_web3")
    assert state
    assert state.state == STATE_ON

    with patch(
        "smarthub.components.nextdns.NextDns.set_setting", return_value=True
    ) as mock_switch_on:
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SERVICE_TURN_OFF,
            {ATTR_ENTITY_ID: "switch.fake_profile_web3"},
            blocking=True,
        )
        await hass.async_block_till_done()

        state = hass.states.get("switch.fake_profile_web3")
        assert state
        assert state.state == STATE_OFF

        mock_switch_on.assert_called_once()


@pytest.mark.parametrize(
    "exc",
    [
        ApiError("API Error"),
        RetryError("Retry Error"),
        TimeoutError,
    ],
)
async def test_availability(hass: SmartHub, exc: Exception) -> None:
    """Ensure that we mark the entities unavailable correctly when service causes an error."""
    await init_integration(hass)

    state = hass.states.get("switch.fake_profile_web3")
    assert state
    assert state.state != STATE_UNAVAILABLE
    assert state.state == STATE_ON

    future = utcnow() + timedelta(minutes=10)
    with patch(
        "smarthub.components.nextdns.NextDns.get_settings",
        side_effect=exc,
    ):
        async_fire_time_changed(hass, future)
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get("switch.fake_profile_web3")
    assert state
    assert state.state == STATE_UNAVAILABLE

    future = utcnow() + timedelta(minutes=20)
    with mock_nextdns():
        async_fire_time_changed(hass, future)
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get("switch.fake_profile_web3")
    assert state
    assert state.state != STATE_UNAVAILABLE
    assert state.state == STATE_ON


@pytest.mark.parametrize(
    "exc",
    [
        ApiError(Mock()),
        TimeoutError,
        ClientConnectorError(Mock(), Mock()),
        ClientError,
    ],
)
async def test_switch_failure(hass: SmartHub, exc: Exception) -> None:
    """Tests that the turn on/off service throws SmartHubError."""
    await init_integration(hass)

    with (
        patch("smarthub.components.nextdns.NextDns.set_setting", side_effect=exc),
        pytest.raises(SmartHubError),
    ):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SERVICE_TURN_ON,
            {ATTR_ENTITY_ID: "switch.fake_profile_block_page"},
            blocking=True,
        )


async def test_switch_auth_error(hass: SmartHub) -> None:
    """Tests that the turn on/off action starts re-auth flow."""
    entry = await init_integration(hass)

    with patch(
        "smarthub.components.nextdns.NextDns.set_setting",
        side_effect=InvalidApiKeyError,
    ):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SERVICE_TURN_ON,
            {ATTR_ENTITY_ID: "switch.fake_profile_block_page"},
            blocking=True,
        )

    assert entry.state is ConfigEntryState.LOADED

    flows = hass.config_entries.flow.async_progress()
    assert len(flows) == 1

    flow = flows[0]
    assert flow.get("step_id") == "reauth_confirm"
    assert flow.get("handler") == DOMAIN

    assert "context" in flow
    assert flow["context"].get("source") == SOURCE_REAUTH
    assert flow["context"].get("entry_id") == entry.entry_id
