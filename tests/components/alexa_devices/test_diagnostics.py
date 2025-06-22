"""Tests for Alexa Devices diagnostics platform."""

from __future__ import annotations

from unittest.mock import AsyncMock

from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from smarthub.components.alexa_devices.const import DOMAIN
from smarthub.core import SmartHub
from smarthub.helpers import device_registry as dr

from . import setup_integration
from .const import TEST_SERIAL_NUMBER

from tests.common import MockConfigEntry
from tests.components.diagnostics import (
    get_diagnostics_for_config_entry,
    get_diagnostics_for_device,
)
from tests.typing import ClientSessionGenerator


async def test_entry_diagnostics(
    hass: SmartHub,
    mock_amazon_devices_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test Amazon config entry diagnostics."""
    await setup_integration(hass, mock_config_entry)

    assert await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    ) == snapshot(
        exclude=props(
            "entry_id",
            "created_at",
            "modified_at",
        )
    )


async def test_device_diagnostics(
    hass: SmartHub,
    mock_amazon_devices_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    hass_client: ClientSessionGenerator,
    device_registry: dr.DeviceRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test Amazon device diagnostics."""
    await setup_integration(hass, mock_config_entry)

    device = device_registry.async_get_device(
        identifiers={(DOMAIN, TEST_SERIAL_NUMBER)}
    )
    assert device, repr(device_registry.devices)

    assert await get_diagnostics_for_device(
        hass, hass_client, mock_config_entry, device
    ) == snapshot(
        exclude=props(
            "entry_id",
            "created_at",
            "modified_at",
        )
    )
