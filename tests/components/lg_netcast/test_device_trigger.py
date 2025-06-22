"""The tests for LG NEtcast device triggers."""

import pytest

from smarthub.components import automation
from smarthub.components.device_automation import DeviceAutomationType
from smarthub.components.device_automation.exceptions import (
    InvalidDeviceAutomationConfig,
)
from smarthub.components.lg_netcast import DOMAIN, device_trigger
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub, ServiceCall
from smarthub.exceptions import SmartHubError
from smarthub.helpers import device_registry as dr
from smarthub.setup import async_setup_component

from . import ENTITY_ID, UNIQUE_ID, setup_lgnetcast

from tests.common import MockConfigEntry, async_get_device_automations


async def test_get_triggers(
    hass: SmartHub, device_registry: dr.DeviceRegistry
) -> None:
    """Test we get the expected triggers."""
    await setup_lgnetcast(hass)

    device = device_registry.async_get_device(identifiers={(DOMAIN, UNIQUE_ID)})
    assert device is not None

    turn_on_trigger = {
        "platform": "device",
        "domain": DOMAIN,
        "type": "lg_netcast.turn_on",
        "device_id": device.id,
        "metadata": {},
    }

    triggers = await async_get_device_automations(
        hass, DeviceAutomationType.TRIGGER, device.id
    )
    assert turn_on_trigger in triggers


async def test_if_fires_on_turn_on_request(
    hass: SmartHub,
    service_calls: list[ServiceCall],
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test for turn_on triggers firing."""
    await setup_lgnetcast(hass)

    device = device_registry.async_get_device(identifiers={(DOMAIN, UNIQUE_ID)})
    assert device is not None

    assert await async_setup_component(
        hass,
        automation.DOMAIN,
        {
            automation.DOMAIN: [
                {
                    "trigger": {
                        "platform": "device",
                        "domain": DOMAIN,
                        "device_id": device.id,
                        "type": "lg_netcast.turn_on",
                    },
                    "action": {
                        "service": "test.automation",
                        "data_template": {
                            "some": "{{ trigger.device_id }}",
                            "id": "{{ trigger.id }}",
                        },
                    },
                },
                {
                    "trigger": {
                        "platform": "lg_netcast.turn_on",
                        "entity_id": ENTITY_ID,
                    },
                    "action": {
                        "service": "test.automation",
                        "data_template": {
                            "some": ENTITY_ID,
                            "id": "{{ trigger.id }}",
                        },
                    },
                },
            ],
        },
    )

    await hass.services.async_call(
        "media_player",
        "turn_on",
        {"entity_id": ENTITY_ID},
        blocking=True,
    )

    await hass.async_block_till_done()
    assert len(service_calls) == 3
    assert service_calls[1].data["some"] == device.id
    assert service_calls[1].data["id"] == 0
    assert service_calls[2].data["some"] == ENTITY_ID
    assert service_calls[2].data["id"] == 0


async def test_failure_scenarios(
    hass: SmartHub, device_registry: dr.DeviceRegistry
) -> None:
    """Test failure scenarios."""
    await setup_lgnetcast(hass)

    # Test wrong trigger platform type
    with pytest.raises(SmartHubError):
        await device_trigger.async_attach_trigger(
            hass, {"type": "wrong.type", "device_id": "invalid_device_id"}, None, {}
        )

    # Test invalid device id
    with pytest.raises(SmartHubError):
        await device_trigger.async_validate_trigger_config(
            hass,
            {
                "platform": "device",
                "domain": DOMAIN,
                "type": "lg_netcast.turn_on",
                "device_id": "invalid_device_id",
            },
        )

    entry = MockConfigEntry(domain="fake", state=ConfigEntryState.LOADED, data={})
    entry.add_to_hass(hass)

    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id, identifiers={("fake", "fake")}
    )

    config = {
        "platform": "device",
        "domain": DOMAIN,
        "device_id": device.id,
        "type": "lg_netcast.turn_on",
    }

    # Test that device id from non lg_netcast domain raises exception
    with pytest.raises(InvalidDeviceAutomationConfig):
        await device_trigger.async_validate_trigger_config(hass, config)

    # Test that only valid triggers are attached
