"""Test the select significant change platform."""

from smarthub.components.select.significant_change import (
    async_check_significant_change,
)
from smarthub.core import SmartHub


async def test_significant_change(hass: SmartHub) -> None:
    """Detect select significant change."""
    attrs1 = {"options": ["option1", "option2"]}
    attrs2 = {"options": ["option1", "option2", "option3"]}

    assert not async_check_significant_change(
        hass, "option1", attrs1, "option1", attrs1
    )
    assert not async_check_significant_change(
        hass, "option1", attrs1, "option1", attrs2
    )
    assert async_check_significant_change(hass, "option1", attrs1, "option2", attrs1)
    assert async_check_significant_change(hass, "option1", attrs1, "option2", attrs2)
