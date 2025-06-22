"""The test for the Coolmaster button platform."""

from __future__ import annotations

from smarthub.components.button import DOMAIN as BUTTON_DOMAIN, SERVICE_PRESS
from smarthub.config_entries import ConfigEntry
from smarthub.const import ATTR_ENTITY_ID
from smarthub.core import SmartHub


async def test_button(
    hass: SmartHub,
    load_int: ConfigEntry,
) -> None:
    """Test the Coolmaster button."""
    assert hass.states.get("binary_sensor.l1_101_clean_filter").state == "on"

    button = hass.states.get("button.l1_101_reset_filter")
    assert button is not None
    await hass.services.async_call(
        BUTTON_DOMAIN,
        SERVICE_PRESS,
        {
            ATTR_ENTITY_ID: button.entity_id,
        },
        blocking=True,
    )
    await hass.async_block_till_done()

    assert hass.states.get("binary_sensor.l1_101_clean_filter").state == "off"
