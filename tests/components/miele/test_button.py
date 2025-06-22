"""Tests for Miele button module."""

from unittest.mock import MagicMock

from aiohttp import ClientResponseError
import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.components.button import DOMAIN as BUTTON_DOMAIN, SERVICE_PRESS
from smarthub.const import ATTR_ENTITY_ID
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers import entity_registry as er

from tests.common import MockConfigEntry, snapshot_platform

TEST_PLATFORM = BUTTON_DOMAIN
pytestmark = pytest.mark.parametrize("platforms", [(TEST_PLATFORM,)])

ENTITY_ID = "button.washing_machine_start"


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_button_states(
    hass: SmartHub,
    mock_miele_client: MagicMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
) -> None:
    """Test button entity state."""

    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_button_states_api_push(
    hass: SmartHub,
    mock_miele_client: MagicMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
    push_data_and_actions: None,
) -> None:
    """Test binary sensor state when the API pushes data via SSE."""

    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_button_press(
    hass: SmartHub,
    mock_miele_client: MagicMock,
    setup_platform: MockConfigEntry,
) -> None:
    """Test button press."""

    await hass.services.async_call(
        TEST_PLATFORM, SERVICE_PRESS, {ATTR_ENTITY_ID: ENTITY_ID}, blocking=True
    )
    mock_miele_client.send_action.assert_called_once_with(
        "Dummy_Appliance_3", {"processAction": 1}
    )


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_api_failure(
    hass: SmartHub,
    mock_miele_client: MagicMock,
    setup_platform: MockConfigEntry,
) -> None:
    """Test handling of exception from API."""
    mock_miele_client.send_action.side_effect = ClientResponseError("test", "Test")

    with pytest.raises(
        SmartHubError, match=f"Failed to set state for {ENTITY_ID}"
    ):
        await hass.services.async_call(
            TEST_PLATFORM, SERVICE_PRESS, {ATTR_ENTITY_ID: ENTITY_ID}, blocking=True
        )
    mock_miele_client.send_action.assert_called_once()
