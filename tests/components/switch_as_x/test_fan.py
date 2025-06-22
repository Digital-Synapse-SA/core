"""Tests for the Switch as X Fan platform."""

from smarthub.components.fan import DOMAIN as FAN_DOMAIN
from smarthub.components.switch import DOMAIN as SWITCH_DOMAIN
from smarthub.components.switch_as_x.config_flow import SwitchAsXConfigFlowHandler
from smarthub.components.switch_as_x.const import (
    CONF_INVERT,
    CONF_TARGET_DOMAIN,
    DOMAIN,
)
from smarthub.const import (
    CONF_ENTITY_ID,
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    Platform,
)
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from tests.common import MockConfigEntry


async def test_default_state(hass: SmartHub) -> None:
    """Test fan switch default state."""
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={
            CONF_ENTITY_ID: "switch.test",
            CONF_INVERT: False,
            CONF_TARGET_DOMAIN: Platform.FAN,
        },
        title="Wind Machine",
        version=SwitchAsXConfigFlowHandler.VERSION,
        minor_version=SwitchAsXConfigFlowHandler.MINOR_VERSION,
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("fan.wind_machine")
    assert state is not None
    assert state.state == "unavailable"
    assert state.attributes["supported_features"] == 48


async def test_service_calls(hass: SmartHub) -> None:
    """Test service calls affecting the switch as fan entity."""
    await async_setup_component(hass, "switch", {"switch": [{"platform": "demo"}]})
    await hass.async_block_till_done()
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={
            CONF_ENTITY_ID: "switch.decorative_lights",
            CONF_INVERT: False,
            CONF_TARGET_DOMAIN: Platform.FAN,
        },
        title="Title is ignored",
        version=SwitchAsXConfigFlowHandler.VERSION,
        minor_version=SwitchAsXConfigFlowHandler.MINOR_VERSION,
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("fan.decorative_lights").state == STATE_ON

    await hass.services.async_call(
        FAN_DOMAIN,
        SERVICE_TOGGLE,
        {CONF_ENTITY_ID: "fan.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("fan.decorative_lights").state == STATE_OFF

    await hass.services.async_call(
        FAN_DOMAIN,
        SERVICE_TURN_ON,
        {CONF_ENTITY_ID: "fan.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_ON
    assert hass.states.get("fan.decorative_lights").state == STATE_ON

    await hass.services.async_call(
        FAN_DOMAIN,
        SERVICE_TURN_OFF,
        {CONF_ENTITY_ID: "fan.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("fan.decorative_lights").state == STATE_OFF

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SERVICE_TURN_ON,
        {CONF_ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_ON
    assert hass.states.get("fan.decorative_lights").state == STATE_ON

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SERVICE_TURN_OFF,
        {CONF_ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("fan.decorative_lights").state == STATE_OFF

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SERVICE_TOGGLE,
        {CONF_ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_ON
    assert hass.states.get("fan.decorative_lights").state == STATE_ON


async def test_service_calls_inverted(hass: SmartHub) -> None:
    """Test service calls affecting the switch as fan entity."""
    await async_setup_component(hass, "switch", {"switch": [{"platform": "demo"}]})
    await hass.async_block_till_done()
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={
            CONF_ENTITY_ID: "switch.decorative_lights",
            CONF_INVERT: True,
            CONF_TARGET_DOMAIN: Platform.FAN,
        },
        title="Title is ignored",
        version=SwitchAsXConfigFlowHandler.VERSION,
        minor_version=SwitchAsXConfigFlowHandler.MINOR_VERSION,
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert hass.states.get("fan.decorative_lights").state == STATE_ON

    await hass.services.async_call(
        FAN_DOMAIN,
        SERVICE_TOGGLE,
        {CONF_ENTITY_ID: "fan.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("fan.decorative_lights").state == STATE_OFF

    await hass.services.async_call(
        FAN_DOMAIN,
        SERVICE_TURN_ON,
        {CONF_ENTITY_ID: "fan.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_ON
    assert hass.states.get("fan.decorative_lights").state == STATE_ON

    await hass.services.async_call(
        FAN_DOMAIN,
        SERVICE_TURN_OFF,
        {CONF_ENTITY_ID: "fan.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("fan.decorative_lights").state == STATE_OFF

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SERVICE_TURN_ON,
        {CONF_ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_ON
    assert hass.states.get("fan.decorative_lights").state == STATE_ON

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SERVICE_TURN_OFF,
        {CONF_ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_OFF
    assert hass.states.get("fan.decorative_lights").state == STATE_OFF

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SERVICE_TOGGLE,
        {CONF_ENTITY_ID: "switch.decorative_lights"},
        blocking=True,
    )

    assert hass.states.get("switch.decorative_lights").state == STATE_ON
    assert hass.states.get("fan.decorative_lights").state == STATE_ON
