"""Test the Fibaro scene platform."""

from unittest.mock import Mock

from smarthub.components.scene import DOMAIN as SCENE_DOMAIN
from smarthub.const import ATTR_ENTITY_ID, SERVICE_TURN_ON
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from .conftest import init_integration

from tests.common import MockConfigEntry


async def test_entity_attributes(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_scene: Mock,
    mock_room: Mock,
) -> None:
    """Test that the attributes of the entity are correct."""
    # Arrange
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_scenes.return_value = [mock_scene]
    # Act
    await init_integration(hass, mock_config_entry)
    # Assert
    entry = entity_registry.async_get("scene.room_1_test_scene")

    assert entry
    assert entry.unique_id == "hc2_111111.scene.1"
    assert entry.original_name == "Room 1 Test scene"


async def test_entity_attributes_without_room(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_scene: Mock,
    mock_room: Mock,
) -> None:
    """Test that the attributes of the entity are correct."""
    # Arrange
    mock_room.name = None
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_scenes.return_value = [mock_scene]
    # Act
    await init_integration(hass, mock_config_entry)
    # Assert
    entry = entity_registry.async_get("scene.unknown_test_scene")

    assert entry
    assert entry.unique_id == "hc2_111111.scene.1"


async def test_activate_scene(
    hass: SmartHub,
    mock_fibaro_client: Mock,
    mock_config_entry: MockConfigEntry,
    mock_scene: Mock,
    mock_room: Mock,
) -> None:
    """Test activate scene is called."""
    # Arrange
    mock_fibaro_client.read_rooms.return_value = [mock_room]
    mock_fibaro_client.read_scenes.return_value = [mock_scene]
    # Act
    await init_integration(hass, mock_config_entry)
    # Act
    await hass.services.async_call(
        SCENE_DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: "scene.room_1_test_scene"},
        blocking=True,
    )
    # Assert
    assert mock_scene.start.call_count == 1
