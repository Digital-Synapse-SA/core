"""Tests for the Elmax switches."""

from unittest.mock import patch

from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import init_integration

from tests.common import snapshot_platform


async def test_switches(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test switches."""
    with patch("smarthub.components.elmax.ELMAX_PLATFORMS", [Platform.SWITCH]):
        entry = await init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
