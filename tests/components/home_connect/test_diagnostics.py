"""Test diagnostics for Home Connect."""

from collections.abc import Awaitable, Callable
from unittest.mock import MagicMock

from syrupy.assertion import SnapshotAssertion

from smarthub.components.home_connect.const import DOMAIN
from smarthub.components.home_connect.diagnostics import (
    async_get_config_entry_diagnostics,
    async_get_device_diagnostics,
)
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub
from smarthub.helpers import device_registry as dr

from tests.common import MockConfigEntry


async def test_async_get_config_entry_diagnostics(
    hass: SmartHub,
    client: MagicMock,
    config_entry: MockConfigEntry,
    integration_setup: Callable[[MagicMock], Awaitable[bool]],
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    assert await integration_setup(client)
    assert config_entry.state is ConfigEntryState.LOADED

    assert await async_get_config_entry_diagnostics(hass, config_entry) == snapshot


async def test_async_get_device_diagnostics(
    hass: SmartHub,
    device_registry: dr.DeviceRegistry,
    client: MagicMock,
    config_entry: MockConfigEntry,
    integration_setup: Callable[[MagicMock], Awaitable[bool]],
    snapshot: SnapshotAssertion,
) -> None:
    """Test device config entry diagnostics."""
    assert await integration_setup(client)
    assert config_entry.state is ConfigEntryState.LOADED

    device = device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(DOMAIN, "SIEMENS-HCS02DWH1-6BE58C26DCC1")},
    )

    assert await async_get_device_diagnostics(hass, config_entry, device) == snapshot
