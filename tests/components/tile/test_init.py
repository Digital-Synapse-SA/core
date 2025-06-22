"""Tests for the Tile integration."""

from unittest.mock import AsyncMock

from syrupy.assertion import SnapshotAssertion

from smarthub.components.tile.const import DOMAIN
from smarthub.core import SmartHub
from smarthub.helpers import device_registry as dr

from . import setup_integration

from tests.common import MockConfigEntry


async def test_device_info(
    hass: SmartHub,
    snapshot: SnapshotAssertion,
    mock_pytile: AsyncMock,
    mock_config_entry: MockConfigEntry,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test device registry integration."""
    await setup_integration(hass, mock_config_entry)
    device_entry = device_registry.async_get_device(
        identifiers={(DOMAIN, "19264d2dffdbca32")}
    )
    assert device_entry is not None
    assert device_entry == snapshot
