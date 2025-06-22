"""Samsung TV trigger dispatcher."""

from __future__ import annotations

from typing import cast

from smarthub.const import CONF_PLATFORM
from smarthub.core import CALLBACK_TYPE, SmartHub
from smarthub.helpers.trigger import (
    TriggerActionType,
    TriggerInfo,
    TriggerProtocol,
)
from smarthub.helpers.typing import ConfigType

from .triggers import turn_on

TRIGGERS = {
    "turn_on": turn_on,
}


def _get_trigger_platform(config: ConfigType) -> TriggerProtocol:
    """Return trigger platform."""
    platform_split = config[CONF_PLATFORM].split(".", maxsplit=1)
    if len(platform_split) < 2 or platform_split[1] not in TRIGGERS:
        raise ValueError(f"Unknown Samsung TV trigger platform {config[CONF_PLATFORM]}")
    return cast(TriggerProtocol, TRIGGERS[platform_split[1]])


async def async_validate_trigger_config(
    hass: SmartHub, config: ConfigType
) -> ConfigType:
    """Validate config."""
    platform = _get_trigger_platform(config)
    return cast(ConfigType, platform.TRIGGER_SCHEMA(config))


async def async_attach_trigger(
    hass: SmartHub,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach trigger of specified platform."""
    platform = _get_trigger_platform(config)
    return await platform.async_attach_trigger(hass, config, action, trigger_info)
