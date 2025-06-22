"""Tests for the Lutron Caseta integration."""

from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import MockBridge, async_setup_integration


async def test_fan_unique_id(
    hass: SmartHub, entity_registry: er.EntityRegistry
) -> None:
    """Test a light unique id."""
    await async_setup_integration(hass, MockBridge)

    fan_entity_id = "fan.master_bedroom_ceiling_fan"

    # Assert that Caseta covers will have the bridge serial hash and the zone id as the uniqueID
    assert entity_registry.async_get(fan_entity_id).unique_id == "000004d2_804"
