"""Tests for Motionblinds BLE init."""

from unittest.mock import patch

from smarthub.components.bluetooth.models import BluetoothServiceInfoBleak
from smarthub.components.motionblinds_ble import options_update_listener
from smarthub.core import SmartHub

from . import setup_integration

from tests.common import MockConfigEntry
from tests.components.bluetooth import inject_bluetooth_service_info


async def test_options_update_listener(
    hass: SmartHub,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test options_update_listener."""

    await setup_integration(hass, mock_config_entry)

    with (
        patch(
            "smarthub.components.motionblinds_ble.MotionDevice.set_custom_disconnect_time"
        ) as mock_set_custom_disconnect_time,
        patch(
            "smarthub.components.motionblinds_ble.MotionDevice.set_permanent_connection"
        ) as set_permanent_connection,
    ):
        await options_update_listener(hass, mock_config_entry)
        mock_set_custom_disconnect_time.assert_called_once()
        set_permanent_connection.assert_called_once()


async def test_update_ble_device(
    hass: SmartHub,
    mock_config_entry: MockConfigEntry,
    service_info: BluetoothServiceInfoBleak,
) -> None:
    """Test async_update_ble_device."""

    await setup_integration(hass, mock_config_entry)

    with patch(
        "smarthub.components.motionblinds_ble.MotionDevice.set_ble_device"
    ) as mock_set_ble_device:
        inject_bluetooth_service_info(hass, service_info)
        mock_set_ble_device.assert_called_once()
