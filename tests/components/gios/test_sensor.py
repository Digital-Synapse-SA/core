"""Test sensor of GIOS integration."""

from copy import deepcopy
from datetime import timedelta
import json
from unittest.mock import patch

from gios import ApiError
from syrupy.assertion import SnapshotAssertion

from smarthub.components.gios.const import DOMAIN
from smarthub.components.sensor import DOMAIN as PLATFORM
from smarthub.const import STATE_UNAVAILABLE, Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er
from smarthub.util.dt import utcnow

from . import init_integration

from tests.common import async_fire_time_changed, async_load_fixture, snapshot_platform


async def test_sensor(
    hass: SmartHub, entity_registry: er.EntityRegistry, snapshot: SnapshotAssertion
) -> None:
    """Test states of the sensor."""
    with patch("smarthub.components.gios.PLATFORMS", [Platform.SENSOR]):
        entry = await init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)


async def test_availability(hass: SmartHub) -> None:
    """Ensure that we mark the entities unavailable correctly when service causes an error."""
    indexes = json.loads(await async_load_fixture(hass, "indexes.json", DOMAIN))
    sensors = json.loads(await async_load_fixture(hass, "sensors.json", DOMAIN))

    await init_integration(hass)

    state = hass.states.get("sensor.home_pm2_5")
    assert state
    assert state.state == "4"

    state = hass.states.get("sensor.home_pm2_5_index")
    assert state
    assert state.state == "good"

    state = hass.states.get("sensor.home_air_quality_index")
    assert state
    assert state.state == "good"

    future = utcnow() + timedelta(minutes=60)
    with patch(
        "smarthub.components.gios.coordinator.Gios._get_all_sensors",
        side_effect=ApiError("Unexpected error"),
    ):
        async_fire_time_changed(hass, future)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.home_pm2_5")
    assert state
    assert state.state == STATE_UNAVAILABLE

    state = hass.states.get("sensor.home_pm2_5_index")
    assert state
    assert state.state == STATE_UNAVAILABLE

    state = hass.states.get("sensor.home_air_quality_index")
    assert state
    assert state.state == STATE_UNAVAILABLE

    incomplete_sensors = deepcopy(sensors)
    incomplete_sensors["pm2.5"] = {}
    future = utcnow() + timedelta(minutes=120)
    with (
        patch(
            "smarthub.components.gios.coordinator.Gios._get_all_sensors",
            return_value=incomplete_sensors,
        ),
        patch(
            "smarthub.components.gios.coordinator.Gios._get_indexes",
            return_value={},
        ),
    ):
        async_fire_time_changed(hass, future)
        await hass.async_block_till_done()

    # There is no PM2.5 data so the state should be unavailable
    state = hass.states.get("sensor.home_pm2_5")
    assert state
    assert state.state == STATE_UNAVAILABLE

    # Indexes are empty so the state should be unavailable
    state = hass.states.get("sensor.home_air_quality_index")
    assert state
    assert state.state == STATE_UNAVAILABLE

    # Indexes are empty so the state should be unavailable
    state = hass.states.get("sensor.home_pm2_5_index")
    assert state
    assert state.state == STATE_UNAVAILABLE

    future = utcnow() + timedelta(minutes=180)
    with (
        patch(
            "smarthub.components.gios.coordinator.Gios._get_all_sensors",
            return_value=sensors,
        ),
        patch(
            "smarthub.components.gios.coordinator.Gios._get_indexes",
            return_value=indexes,
        ),
    ):
        async_fire_time_changed(hass, future)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.home_pm2_5")
    assert state
    assert state.state == "4"

    state = hass.states.get("sensor.home_pm2_5_index")
    assert state
    assert state.state == "good"

    state = hass.states.get("sensor.home_air_quality_index")
    assert state
    assert state.state == "good"


async def test_invalid_indexes(hass: SmartHub) -> None:
    """Test states of the sensor when API returns invalid indexes."""
    await init_integration(hass, invalid_indexes=True)

    state = hass.states.get("sensor.home_nitrogen_dioxide_index")
    assert state
    assert state.state == STATE_UNAVAILABLE

    state = hass.states.get("sensor.home_ozone_index")
    assert state
    assert state.state == STATE_UNAVAILABLE

    state = hass.states.get("sensor.home_pm10_index")
    assert state
    assert state.state == STATE_UNAVAILABLE

    state = hass.states.get("sensor.home_pm2_5_index")
    assert state
    assert state.state == STATE_UNAVAILABLE

    state = hass.states.get("sensor.home_sulphur_dioxide_index")
    assert state
    assert state.state == STATE_UNAVAILABLE

    state = hass.states.get("sensor.home_air_quality_index")
    assert state is None


async def test_unique_id_migration(
    hass: SmartHub, entity_registry: er.EntityRegistry
) -> None:
    """Test states of the unique_id migration."""
    entity_registry.async_get_or_create(
        PLATFORM,
        DOMAIN,
        "123-pm2.5",
        suggested_object_id="home_pm2_5",
        disabled_by=None,
    )

    await init_integration(hass)

    entry = entity_registry.async_get("sensor.home_pm2_5")
    assert entry
    assert entry.unique_id == "123-pm25"
