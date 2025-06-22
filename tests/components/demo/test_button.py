"""The tests for the demo button component."""

from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
import pytest

from smarthub.components.button import DOMAIN as BUTTON_DOMAIN, SERVICE_PRESS
from smarthub.const import ATTR_ENTITY_ID, STATE_UNKNOWN, Platform
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component
from smarthub.util import dt as dt_util

ENTITY_PUSH = "button.push"


@pytest.fixture
async def button_only() -> None:
    """Enable only the button platform."""
    with patch(
        "smarthub.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.BUTTON],
    ):
        yield


@pytest.fixture(autouse=True)
async def setup_demo_button(hass: SmartHub, button_only) -> None:
    """Initialize setup demo button entity."""
    assert await async_setup_component(
        hass, BUTTON_DOMAIN, {"button": {"platform": "demo"}}
    )
    await hass.async_block_till_done()


def test_setup_params(hass: SmartHub) -> None:
    """Test the initial parameters."""
    state = hass.states.get(ENTITY_PUSH)
    assert state
    assert state.state == STATE_UNKNOWN


async def test_press(hass: SmartHub, freezer: FrozenDateTimeFactory) -> None:
    """Test pressing the button."""
    state = hass.states.get(ENTITY_PUSH)
    assert state
    assert state.state == STATE_UNKNOWN

    now = dt_util.parse_datetime("2021-01-09 12:00:00+00:00")
    freezer.move_to(now)
    await hass.services.async_call(
        BUTTON_DOMAIN,
        SERVICE_PRESS,
        {ATTR_ENTITY_ID: ENTITY_PUSH},
        blocking=True,
    )

    state = hass.states.get(ENTITY_PUSH)
    assert state
    assert state.state == now.isoformat()
