"""The tests for the demo date component."""

from unittest.mock import patch

import pytest

from smarthub.components.date import (
    ATTR_DATE,
    DOMAIN as DATE_DOMAIN,
    SERVICE_SET_VALUE,
)
from smarthub.const import ATTR_ENTITY_ID, Platform
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

ENTITY_DATE = "date.date"


@pytest.fixture
async def date_only() -> None:
    """Enable only the date platform."""
    with patch(
        "smarthub.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.DATE],
    ):
        yield


@pytest.fixture(autouse=True)
async def setup_demo_date(hass: SmartHub, date_only) -> None:
    """Initialize setup demo date."""
    assert await async_setup_component(
        hass, DATE_DOMAIN, {"date": {"platform": "demo"}}
    )
    await hass.async_block_till_done()


def test_setup_params(hass: SmartHub) -> None:
    """Test the initial parameters."""
    state = hass.states.get(ENTITY_DATE)
    assert state.state == "2020-01-01"


async def test_set_datetime(hass: SmartHub) -> None:
    """Test set datetime service."""
    await hass.services.async_call(
        DATE_DOMAIN,
        SERVICE_SET_VALUE,
        {ATTR_ENTITY_ID: ENTITY_DATE, ATTR_DATE: "2021-02-03"},
        blocking=True,
    )
    state = hass.states.get(ENTITY_DATE)
    assert state.state == "2021-02-03"
