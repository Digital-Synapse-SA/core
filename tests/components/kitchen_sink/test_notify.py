"""The tests for the demo button component."""

from collections.abc import AsyncGenerator
from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
import pytest

from smarthub.components.kitchen_sink import DOMAIN
from smarthub.components.notify import (
    ATTR_MESSAGE,
    DOMAIN as NOTIFY_DOMAIN,
    SERVICE_SEND_MESSAGE,
)
from smarthub.const import ATTR_ENTITY_ID, STATE_UNKNOWN, Platform
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component
from smarthub.util import dt as dt_util

ENTITY_DIRECT_MESSAGE = "notify.mybox_personal_notifier"


@pytest.fixture
async def notify_only() -> AsyncGenerator[None]:
    """Enable only the button platform."""
    with patch(
        "smarthub.components.kitchen_sink.COMPONENTS_WITH_DEMO_PLATFORM",
        [Platform.NOTIFY],
    ):
        yield


@pytest.fixture(autouse=True)
async def setup_comp(hass: SmartHub, notify_only: None):
    """Set up demo component."""
    assert await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
    await hass.async_block_till_done()


def test_setup_params(hass: SmartHub) -> None:
    """Test the initial parameters."""
    state = hass.states.get(ENTITY_DIRECT_MESSAGE)
    assert state
    assert state.state == STATE_UNKNOWN


async def test_send_message(
    hass: SmartHub, freezer: FrozenDateTimeFactory
) -> None:
    """Test pressing the button."""
    state = hass.states.get(ENTITY_DIRECT_MESSAGE)
    assert state
    assert state.state == STATE_UNKNOWN

    now = dt_util.parse_datetime("2021-01-09 12:00:00+00:00")
    freezer.move_to(now)
    await hass.services.async_call(
        NOTIFY_DOMAIN,
        SERVICE_SEND_MESSAGE,
        {ATTR_ENTITY_ID: ENTITY_DIRECT_MESSAGE, ATTR_MESSAGE: "You have an update!"},
        blocking=True,
    )

    state = hass.states.get(ENTITY_DIRECT_MESSAGE)
    assert state
    assert state.state == now.isoformat()
