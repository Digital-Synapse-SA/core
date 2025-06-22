"""The button tests for the yale platform."""

from smarthub.components.button import DOMAIN as BUTTON_DOMAIN, SERVICE_PRESS
from smarthub.const import ATTR_ENTITY_ID
from smarthub.core import SmartHub

from .mocks import _create_yale_api_with_devices, _mock_lock_from_fixture


async def test_wake_lock(hass: SmartHub) -> None:
    """Test creation of a lock and wake it."""
    lock_one = await _mock_lock_from_fixture(
        hass, "get_lock.online_with_doorsense.json"
    )
    _, api_instance, _ = await _create_yale_api_with_devices(hass, [lock_one])
    entity_id = "button.online_with_doorsense_name_wake"
    binary_sensor_online_with_doorsense_name = hass.states.get(entity_id)
    assert binary_sensor_online_with_doorsense_name is not None
    api_instance.async_status_async.reset_mock()
    await hass.services.async_call(
        BUTTON_DOMAIN, SERVICE_PRESS, {ATTR_ENTITY_ID: entity_id}, blocking=True
    )
    api_instance.async_status_async.assert_called_once()
