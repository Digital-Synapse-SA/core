"""Tests for Motionblinds BLE entities."""

from unittest.mock import Mock

import pytest

from smarthub.components.smarthub import (
    DOMAIN as HA_DOMAIN,
    SERVICE_UPDATE_ENTITY,
)
from smarthub.components.motionblinds_ble.const import (
    ATTR_CONNECT,
    ATTR_DISCONNECT,
    ATTR_FAVORITE,
    ATTR_SPEED,
)
from smarthub.const import ATTR_ENTITY_ID, Platform
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from . import setup_integration

from tests.common import MockConfigEntry


@pytest.mark.usefixtures("motionblinds_ble_connect")
@pytest.mark.parametrize(
    ("platform", "entity"),
    [
        (Platform.BUTTON, ATTR_CONNECT),
        (Platform.BUTTON, ATTR_DISCONNECT),
        (Platform.BUTTON, ATTR_FAVORITE),
        (Platform.SELECT, ATTR_SPEED),
    ],
)
async def test_entity_update(
    hass: SmartHub,
    mock_config_entry: MockConfigEntry,
    mock_motion_device: Mock,
    name: str,
    platform: Platform,
    entity: str,
) -> None:
    """Test updating entity using smarthub.update_entity."""

    await async_setup_component(hass, HA_DOMAIN, {})
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        HA_DOMAIN,
        SERVICE_UPDATE_ENTITY,
        {ATTR_ENTITY_ID: f"{platform.name.lower()}.{name}_{entity}"},
        blocking=True,
    )
    mock_motion_device.status_query.assert_called_once_with()
