"""Tests for the Palazzetti button platform."""

from unittest.mock import AsyncMock, patch

from pypalazzetti.exceptions import CommunicationError
import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.components.button import DOMAIN as BUTTON_DOMAIN, SERVICE_PRESS
from smarthub.const import ATTR_ENTITY_ID, Platform
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers import entity_registry as er

from . import setup_integration

from tests.common import MockConfigEntry, snapshot_platform

ENTITY_ID = "button.stove_silent"


async def test_all_entities(
    hass: SmartHub,
    snapshot: SnapshotAssertion,
    mock_palazzetti_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("smarthub.components.palazzetti.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_async_press(
    hass: SmartHub,
    mock_palazzetti_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test pressing via service call."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        BUTTON_DOMAIN,
        SERVICE_PRESS,
        {ATTR_ENTITY_ID: ENTITY_ID},
        blocking=True,
    )
    mock_palazzetti_client.set_fan_silent.assert_called_once()


async def test_async_press_error(
    hass: SmartHub,
    mock_palazzetti_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test pressing with error via service call."""
    await setup_integration(hass, mock_config_entry)

    mock_palazzetti_client.set_fan_silent.side_effect = CommunicationError()
    error_message = "Could not connect to the device"
    with pytest.raises(SmartHubError, match=error_message):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            SERVICE_PRESS,
            {ATTR_ENTITY_ID: ENTITY_ID},
            blocking=True,
        )
