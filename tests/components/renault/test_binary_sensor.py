"""Tests for Renault binary sensors."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from syrupy.assertion import SnapshotAssertion

from smarthub.config_entries import ConfigEntry
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from tests.common import snapshot_platform

pytestmark = pytest.mark.usefixtures("patch_renault_account", "patch_get_vehicles")


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override PLATFORMS."""
    with patch("smarthub.components.renault.PLATFORMS", [Platform.BINARY_SENSOR]):
        yield


@pytest.mark.usefixtures("fixtures_with_data")
async def test_binary_sensors(
    hass: SmartHub,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for Renault binary sensors."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.usefixtures("fixtures_with_no_data")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_binary_sensor_empty(
    hass: SmartHub,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for Renault binary sensors with empty data from Renault."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.usefixtures("fixtures_with_invalid_upstream_exception")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_binary_sensor_errors(
    hass: SmartHub,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test for Renault binary sensors with temporary failure."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.usefixtures("fixtures_with_access_denied_exception")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_binary_sensor_access_denied(
    hass: SmartHub,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test for Renault binary sensors with access denied failure."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert len(entity_registry.entities) == 0


@pytest.mark.usefixtures("fixtures_with_not_supported_exception")
@pytest.mark.parametrize("vehicle_type", ["zoe_40"], indirect=True)
async def test_binary_sensor_not_supported(
    hass: SmartHub,
    config_entry: ConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test for Renault binary sensors with not supported failure."""
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert len(entity_registry.entities) == 0
