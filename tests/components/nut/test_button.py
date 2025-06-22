"""Test the NUT button platform."""

import pytest

from smarthub.components.button import DOMAIN as BUTTON_DOMAIN, SERVICE_PRESS
from smarthub.components.nut.const import INTEGRATION_SUPPORTED_COMMANDS
from smarthub.const import ATTR_ENTITY_ID, STATE_UNKNOWN
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from .util import async_init_integration


@pytest.mark.parametrize(
    "model",
    [
        "CP1350C",
        "5E650I",
        "5E850I",
        "CP1500PFCLCD",
        "DL650ELCD",
        "EATON5P1550",
        "blazer_usb",
    ],
)
async def test_buttons_ups(
    hass: SmartHub, entity_registry: er.EntityRegistry, model: str
) -> None:
    """Tests that there are no standard buttons."""

    list_commands_return_value = {
        supported_command: supported_command
        for supported_command in INTEGRATION_SUPPORTED_COMMANDS
    }

    await async_init_integration(
        hass,
        model,
        list_commands_return_value=list_commands_return_value,
    )

    button = hass.states.get("button.ups1_power_cycle_outlet_1")
    assert not button


@pytest.mark.parametrize(
    ("model", "unique_id_base"),
    [
        (
            "EATON-EPDU-G3",
            "EATON_ePDU MA 00U-C IN: TYPE 00A 0P OUT: 00xTYPE_A000A00000_",
        ),
    ],
)
async def test_buttons_pdu_dynamic_outlets(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    model: str,
    unique_id_base: str,
) -> None:
    """Tests that the button entities are correct."""

    list_commands_return_value = {
        supported_command: supported_command
        for supported_command in INTEGRATION_SUPPORTED_COMMANDS
    }

    for num in range(1, 25):
        command = f"outlet.{num!s}.load.cycle"
        list_commands_return_value[command] = command

    await async_init_integration(
        hass,
        model,
        list_commands_return_value=list_commands_return_value,
    )

    entity_id = "button.ups1_power_cycle_outlet_a1"
    entry = entity_registry.async_get(entity_id)
    assert entry
    assert entry.unique_id == f"{unique_id_base}outlet.1.load.cycle"

    button = hass.states.get(entity_id)
    assert button
    assert button.state == STATE_UNKNOWN

    await hass.services.async_call(
        BUTTON_DOMAIN,
        SERVICE_PRESS,
        {ATTR_ENTITY_ID: entity_id},
        blocking=True,
    )
    await hass.async_block_till_done()

    button = hass.states.get(entity_id)
    assert button.state != STATE_UNKNOWN

    button = hass.states.get("button.ups1_power_cycle_outlet_25")
    assert not button

    button = hass.states.get("button.ups1_power_cycle_outlet_a25")
    assert not button
