"""Tests for the plaato binary sensors."""

from unittest.mock import patch

from pyplaato.models.device import PlaatoDeviceType
import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import init_integration

from tests.common import snapshot_platform


# note: PlaatoDeviceType.Airlock does not provide binary sensors
@pytest.mark.parametrize("device_type", [PlaatoDeviceType.Keg])
async def test_binary_sensors(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    device_type: PlaatoDeviceType,
) -> None:
    """Test binary sensors."""
    with patch(
        "smarthub.components.plaato.PLATFORMS",
        [Platform.BINARY_SENSOR],
    ):
        entry = await init_integration(hass, device_type)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
