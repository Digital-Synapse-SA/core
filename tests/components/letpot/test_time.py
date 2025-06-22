"""Test time entities for the LetPot integration."""

from datetime import time
from unittest.mock import MagicMock, patch

from letpot.exceptions import LetPotConnectionException, LetPotException
import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.components.time import SERVICE_SET_VALUE
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry, snapshot_platform


async def test_all_entities(
    hass: SmartHub,
    snapshot: SnapshotAssertion,
    mock_client: MagicMock,
    mock_device_client: MagicMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test time entities."""
    with patch("smarthub.components.letpot.PLATFORMS", [Platform.TIME]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_set_time(
    hass: SmartHub,
    mock_config_entry: MockConfigEntry,
    mock_client: MagicMock,
    mock_device_client: MagicMock,
) -> None:
    """Test setting the time entity."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        "time",
        SERVICE_SET_VALUE,
        service_data={"time": time(hour=7, minute=0)},
        blocking=True,
        target={"entity_id": "time.garden_light_on"},
    )

    mock_device_client.set_light_schedule.assert_awaited_once_with(time(7, 0), None)


@pytest.mark.parametrize(
    ("exception", "user_error"),
    [
        (
            LetPotConnectionException("Connection failed"),
            "An error occurred while communicating with the LetPot device: Connection failed",
        ),
        (
            LetPotException("Random thing failed"),
            "An unknown error occurred while communicating with the LetPot device: Random thing failed",
        ),
    ],
)
async def test_time_error(
    hass: SmartHub,
    mock_config_entry: MockConfigEntry,
    mock_client: MagicMock,
    mock_device_client: MagicMock,
    exception: Exception,
    user_error: str,
) -> None:
    """Test time entity exception handling."""
    await setup_integration(hass, mock_config_entry)

    mock_device_client.set_light_schedule.side_effect = exception

    assert hass.states.get("time.garden_light_on") is not None
    with pytest.raises(SmartHubError, match=user_error):
        await hass.services.async_call(
            "time",
            SERVICE_SET_VALUE,
            service_data={"time": time(hour=7, minute=0)},
            blocking=True,
            target={"entity_id": "time.garden_light_on"},
        )
