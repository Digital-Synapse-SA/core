"""Test the Fibaro sensor platform."""

from unittest.mock import Mock, patch

from smarthub.components.sensor import SensorDeviceClass
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from .conftest import init_integration

from tests.common import MockConfigEntry


async def test_power_sensor_detected(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_power_sensor: Mock,
    mock_room: Mock,
) -> None:
    """Test that the strange power entity is detected.

    Similar to a Qubino 3-Phase power meter.
    """
    # Arrange
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_devices.return_value = [mock_power_sensor]

    with patch("smarthub.components.fibaro.PLATFORMS", [Platform.SENSOR]):
        # Act
        await init_integration(hass, mock_config_entry)
        # Assert
        entry = entity_registry.async_get("sensor.room_1_test_sensor_1_power")
        assert entry
        assert entry.unique_id == "hc2_111111.1_power"
        assert entry.original_name == "Room 1 Test sensor Power"
        assert entry.original_device_class == SensorDeviceClass.POWER
