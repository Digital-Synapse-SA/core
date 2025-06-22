"""Test Subaru locks."""

from unittest.mock import patch

import pytest
from voluptuous.error import MultipleInvalid

from smarthub.components.lock import DOMAIN as LOCK_DOMAIN
from smarthub.components.subaru.const import (
    ATTR_DOOR,
    DOMAIN,
    SERVICE_UNLOCK_SPECIFIC_DOOR,
    UNLOCK_DOOR_DRIVERS,
)
from smarthub.const import ATTR_ENTITY_ID, SERVICE_LOCK, SERVICE_UNLOCK
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers import entity_registry as er

from .conftest import MOCK_API

MOCK_API_LOCK = f"{MOCK_API}lock"
MOCK_API_UNLOCK = f"{MOCK_API}unlock"
DEVICE_ID = "lock.test_vehicle_2_door_locks"


async def test_device_exists(
    hass: SmartHub, entity_registry: er.EntityRegistry, ev_entry
) -> None:
    """Test subaru lock entity exists."""
    entry = entity_registry.async_get(DEVICE_ID)
    assert entry


async def test_lock_cmd(hass: SmartHub, ev_entry) -> None:
    """Test subaru lock function."""
    with patch(MOCK_API_LOCK) as mock_lock:
        await hass.services.async_call(
            LOCK_DOMAIN, SERVICE_LOCK, {ATTR_ENTITY_ID: DEVICE_ID}, blocking=True
        )
        await hass.async_block_till_done()
        mock_lock.assert_called_once()


async def test_unlock_cmd(hass: SmartHub, ev_entry) -> None:
    """Test subaru unlock function."""
    with patch(MOCK_API_UNLOCK) as mock_unlock:
        await hass.services.async_call(
            LOCK_DOMAIN, SERVICE_UNLOCK, {ATTR_ENTITY_ID: DEVICE_ID}, blocking=True
        )
        await hass.async_block_till_done()
        mock_unlock.assert_called_once()


async def test_lock_cmd_fails(hass: SmartHub, ev_entry) -> None:
    """Test subaru lock request that initiates but fails."""
    with (
        patch(MOCK_API_LOCK, return_value=False) as mock_lock,
        pytest.raises(SmartHubError),
    ):
        await hass.services.async_call(
            LOCK_DOMAIN, SERVICE_UNLOCK, {ATTR_ENTITY_ID: DEVICE_ID}, blocking=True
        )
    mock_lock.assert_not_called()


async def test_unlock_specific_door(hass: SmartHub, ev_entry) -> None:
    """Test subaru unlock specific door function."""
    with patch(MOCK_API_UNLOCK) as mock_unlock:
        await hass.services.async_call(
            DOMAIN,
            SERVICE_UNLOCK_SPECIFIC_DOOR,
            {ATTR_ENTITY_ID: DEVICE_ID, ATTR_DOOR: UNLOCK_DOOR_DRIVERS},
            blocking=True,
        )
        await hass.async_block_till_done()
        mock_unlock.assert_called_once()


async def test_unlock_specific_door_invalid(hass: SmartHub, ev_entry) -> None:
    """Test subaru unlock specific door function."""
    with patch(MOCK_API_UNLOCK) as mock_unlock, pytest.raises(MultipleInvalid):
        await hass.services.async_call(
            DOMAIN,
            SERVICE_UNLOCK_SPECIFIC_DOOR,
            {ATTR_ENTITY_ID: DEVICE_ID, ATTR_DOOR: "bad_value"},
            blocking=True,
        )
    mock_unlock.assert_not_called()
