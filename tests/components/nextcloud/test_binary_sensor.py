"""Tests for the Nextcloud binary sensors."""

from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import init_integration
from .const import NC_DATA, VALID_CONFIG

from tests.common import snapshot_platform


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_async_setup_entry(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test a successful setup entry."""
    with patch(
        "smarthub.components.nextcloud.PLATFORMS", [Platform.BINARY_SENSOR]
    ):
        entry = await init_integration(hass, VALID_CONFIG, NC_DATA)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
