"""The tests for the Air Quality component."""

import pytest

from smarthub.components.air_quality import ATTR_N2O, ATTR_OZONE, ATTR_PM_10
from smarthub.const import (
    ATTR_ATTRIBUTION,
    ATTR_UNIT_OF_MEASUREMENT,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
)
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component


@pytest.fixture(autouse=True)
async def setup_smarthub(hass: SmartHub):
    """Set up the smarthub integration."""
    await async_setup_component(hass, "smarthub", {})


async def test_state(hass: SmartHub) -> None:
    """Test Air Quality state."""
    config = {"air_quality": {"platform": "demo"}}

    assert await async_setup_component(hass, "air_quality", config)
    await hass.async_block_till_done()

    state = hass.states.get("air_quality.demo_air_quality_home")
    assert state is not None

    assert state.state == "14"


async def test_attributes(hass: SmartHub) -> None:
    """Test Air Quality attributes."""
    config = {"air_quality": {"platform": "demo"}}

    assert await async_setup_component(hass, "air_quality", config)
    await hass.async_block_till_done()

    state = hass.states.get("air_quality.demo_air_quality_office")
    assert state is not None

    data = state.attributes
    assert data.get(ATTR_PM_10) == 16
    assert data.get(ATTR_N2O) is None
    assert data.get(ATTR_OZONE) is None
    assert data.get(ATTR_ATTRIBUTION) == "Powered by SmartHub"
    assert (
        data.get(ATTR_UNIT_OF_MEASUREMENT) == CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
    )
