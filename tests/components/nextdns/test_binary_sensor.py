"""Test binary sensor of NextDNS integration."""

from datetime import timedelta
from unittest.mock import patch

from nextdns import ApiError
from syrupy.assertion import SnapshotAssertion

from smarthub.const import STATE_ON, STATE_UNAVAILABLE, Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er
from smarthub.util.dt import utcnow

from . import init_integration, mock_nextdns

from tests.common import async_fire_time_changed, snapshot_platform


async def test_binary_sensor(
    hass: SmartHub, entity_registry: er.EntityRegistry, snapshot: SnapshotAssertion
) -> None:
    """Test states of the binary sensors."""
    with patch("smarthub.components.nextdns.PLATFORMS", [Platform.BINARY_SENSOR]):
        entry = await init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)


async def test_availability(hass: SmartHub) -> None:
    """Ensure that we mark the entities unavailable correctly when service causes an error."""
    await init_integration(hass)

    state = hass.states.get("binary_sensor.fake_profile_device_connection_status")
    assert state
    assert state.state != STATE_UNAVAILABLE
    assert state.state == STATE_ON

    future = utcnow() + timedelta(minutes=10)
    with patch(
        "smarthub.components.nextdns.NextDns.connection_status",
        side_effect=ApiError("API Error"),
    ):
        async_fire_time_changed(hass, future)
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get("binary_sensor.fake_profile_device_connection_status")
    assert state
    assert state.state == STATE_UNAVAILABLE

    future = utcnow() + timedelta(minutes=20)
    with mock_nextdns():
        async_fire_time_changed(hass, future)
        await hass.async_block_till_done(wait_background_tasks=True)

    state = hass.states.get("binary_sensor.fake_profile_device_connection_status")
    assert state
    assert state.state != STATE_UNAVAILABLE
    assert state.state == STATE_ON
