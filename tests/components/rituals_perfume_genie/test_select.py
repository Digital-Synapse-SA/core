"""Tests for the Rituals Perfume Genie select platform."""

import pytest

from smarthub.components.smarthub import SERVICE_UPDATE_ENTITY
from smarthub.components.select import (
    ATTR_OPTION,
    ATTR_OPTIONS,
    DOMAIN as SELECT_DOMAIN,
)
from smarthub.const import (
    ATTR_ENTITY_ID,
    SERVICE_SELECT_OPTION,
    EntityCategory,
    UnitOfArea,
)
from smarthub.core import SmartHub
from smarthub.exceptions import ServiceValidationError
from smarthub.helpers import entity_registry as er
from smarthub.setup import async_setup_component

from .common import init_integration, mock_config_entry, mock_diffuser


async def test_select_entity(
    hass: SmartHub, entity_registry: er.EntityRegistry
) -> None:
    """Test the creation and state of the diffuser select entity."""
    config_entry = mock_config_entry(unique_id="select_test")
    diffuser = mock_diffuser(hublot="lot123", room_size_square_meter=60)
    await init_integration(hass, config_entry, [diffuser])

    state = hass.states.get("select.genie_room_size")
    assert state
    assert state.state == str(diffuser.room_size_square_meter)
    assert state.attributes[ATTR_OPTIONS] == ["15", "30", "60", "100"]

    entry = entity_registry.async_get("select.genie_room_size")
    assert entry
    assert entry.unique_id == f"{diffuser.hublot}-room_size_square_meter"
    assert entry.unit_of_measurement == UnitOfArea.SQUARE_METERS
    assert entry.entity_category == EntityCategory.CONFIG


async def test_select_option(hass: SmartHub) -> None:
    """Test selecting of a option."""
    config_entry = mock_config_entry(unique_id="select_invalid_option_test")
    diffuser = mock_diffuser(hublot="lot123", room_size_square_meter=60)
    await init_integration(hass, config_entry, [diffuser])
    await async_setup_component(hass, "smarthub", {})
    diffuser.room_size_square_meter = 30

    state = hass.states.get("select.genie_room_size")
    assert state
    assert state.state == "60"

    await hass.services.async_call(
        SELECT_DOMAIN,
        SERVICE_SELECT_OPTION,
        {ATTR_ENTITY_ID: "select.genie_room_size", ATTR_OPTION: "30"},
        blocking=True,
    )
    await hass.services.async_call(
        "smarthub",
        SERVICE_UPDATE_ENTITY,
        {ATTR_ENTITY_ID: ["select.genie_room_size"]},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get("select.genie_room_size")
    assert state
    assert state.state == "30"


async def test_select_invalid_option(hass: SmartHub) -> None:
    """Test selecting an invalid option."""
    config_entry = mock_config_entry(unique_id="select_invalid_option_test")
    diffuser = mock_diffuser(hublot="lot123", room_size_square_meter=60)
    await init_integration(hass, config_entry, [diffuser])
    await async_setup_component(hass, "smarthub", {})

    state = hass.states.get("select.genie_room_size")
    assert state
    assert state.state == "60"

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            SELECT_DOMAIN,
            SERVICE_SELECT_OPTION,
            {ATTR_ENTITY_ID: "select.genie_room_size", ATTR_OPTION: "120"},
            blocking=True,
        )
    await hass.services.async_call(
        "smarthub",
        SERVICE_UPDATE_ENTITY,
        {ATTR_ENTITY_ID: ["select.genie_room_size"]},
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get("select.genie_room_size")
    assert state
    assert state.state == "60"
