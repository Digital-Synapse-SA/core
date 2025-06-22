"""Provides device automations for Arcam FMJ Receiver control."""

from __future__ import annotations

import voluptuous as vol

from smarthub.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from smarthub.const import (
    ATTR_ENTITY_ID,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_PLATFORM,
    CONF_TYPE,
)
from smarthub.core import CALLBACK_TYPE, Event, HassJob, SmartHub, callback
from smarthub.helpers import config_validation as cv, entity_registry as er
from smarthub.helpers.trigger import TriggerActionType, TriggerInfo
from smarthub.helpers.typing import ConfigType

from .const import DOMAIN, EVENT_TURN_ON

TRIGGER_TYPES = {"turn_on"}
TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_ENTITY_ID): cv.entity_id_or_uuid,
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
    }
)


async def async_get_triggers(
    hass: SmartHub, device_id: str
) -> list[dict[str, str]]:
    """List device triggers for Arcam FMJ Receiver control devices."""
    entity_registry = er.async_get(hass)

    return [
        {
            CONF_PLATFORM: "device",
            CONF_DEVICE_ID: device_id,
            CONF_DOMAIN: DOMAIN,
            CONF_ENTITY_ID: entry.id,
            CONF_TYPE: "turn_on",
        }
        for entry in er.async_entries_for_device(entity_registry, device_id)
        if entry.domain == "media_player"
    ]


async def async_attach_trigger(
    hass: SmartHub,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    trigger_data = trigger_info["trigger_data"]
    job = HassJob(action)

    if config[CONF_TYPE] == "turn_on":
        registry = er.async_get(hass)
        entity_id = er.async_resolve_entity_id(registry, config[ATTR_ENTITY_ID])

        @callback
        def _handle_event(event: Event) -> None:
            if event.data[ATTR_ENTITY_ID] == entity_id:
                hass.async_run_hass_job(
                    job,
                    {
                        "trigger": {
                            **trigger_data,
                            **config,
                            "description": f"{DOMAIN} - {entity_id}",
                            "entity_id": entity_id,
                        }
                    },
                    event.context,
                )

        return hass.bus.async_listen(EVENT_TURN_ON, _handle_event)

    return lambda: None
