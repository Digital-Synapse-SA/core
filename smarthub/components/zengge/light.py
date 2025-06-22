"""Support for Zengge lights."""

from __future__ import annotations

import voluptuous as vol

from smarthub.components.light import PLATFORM_SCHEMA as LIGHT_PLATFORM_SCHEMA
from smarthub.const import CONF_DEVICES, CONF_NAME
from smarthub.core import SmartHub
from smarthub.helpers import config_validation as cv, issue_registry as ir
from smarthub.helpers.entity_platform import AddEntitiesCallback
from smarthub.helpers.typing import ConfigType, DiscoveryInfoType

DEVICE_SCHEMA = vol.Schema({vol.Optional(CONF_NAME): cv.string})
DOMAIN = "zengge"

PLATFORM_SCHEMA = LIGHT_PLATFORM_SCHEMA.extend(
    {vol.Optional(CONF_DEVICES, default={}): {cv.string: DEVICE_SCHEMA}}
)


def async_setup_platform(
    hass: SmartHub,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Zengge platform."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        DOMAIN,
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="integration_removed",
        translation_placeholders={
            "led_ble_url": "https://www.smart-hub.io/integrations/led_ble/",
        },
    )
