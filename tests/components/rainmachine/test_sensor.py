"""Test RainMachine sensors."""

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.components.rainmachine import DOMAIN
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er
from smarthub.setup import async_setup_component

from tests.common import MockConfigEntry, snapshot_platform


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensors(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    config: dict[str, Any],
    config_entry: MockConfigEntry,
    client: AsyncMock,
) -> None:
    """Test sensors."""
    with (
        patch("smarthub.components.rainmachine.Client", return_value=client),
        patch("smarthub.components.rainmachine.PLATFORMS", [Platform.SENSOR]),
    ):
        assert await async_setup_component(hass, DOMAIN, config)
        await hass.async_block_till_done()
    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)
