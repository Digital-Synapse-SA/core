"""SmartHub trigger dispatcher."""

from typing import cast

from smarthub.const import CONF_PLATFORM
from smarthub.core import CALLBACK_TYPE, SmartHub
from smarthub.helpers.importlib import async_import_module
from smarthub.helpers.trigger import (
    TriggerActionType,
    TriggerInfo,
    TriggerProtocol,
)
from smarthub.helpers.typing import ConfigType


async def _async_get_trigger_platform(
    hass: SmartHub, platform_name: str
) -> TriggerProtocol:
    """Get trigger platform from cache or import it."""
    platform = await async_import_module(
        hass, f"smarthub.components.smarthub.triggers.{platform_name}"
    )
    return cast(TriggerProtocol, platform)


async def async_validate_trigger_config(
    hass: SmartHub, config: ConfigType
) -> ConfigType:
    """Validate config."""
    platform = await _async_get_trigger_platform(hass, config[CONF_PLATFORM])
    if hasattr(platform, "async_validate_trigger_config"):
        return await platform.async_validate_trigger_config(hass, config)

    return platform.TRIGGER_SCHEMA(config)  # type: ignore[no-any-return]


async def async_attach_trigger(
    hass: SmartHub,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach trigger of specified platform."""
    platform = await _async_get_trigger_platform(hass, config[CONF_PLATFORM])
    return await platform.async_attach_trigger(hass, config, action, trigger_info)
