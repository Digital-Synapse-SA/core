"""The tests for number recorder."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

import pytest

from smarthub.components import number
from smarthub.components.number import ATTR_MAX, ATTR_MIN, ATTR_MODE, ATTR_STEP
from smarthub.components.recorder import Recorder
from smarthub.components.recorder.history import get_significant_states
from smarthub.const import ATTR_FRIENDLY_NAME, Platform
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component
from smarthub.util import dt as dt_util

from tests.common import async_fire_time_changed
from tests.components.recorder.common import async_wait_recording_done


@pytest.fixture(autouse=True)
async def number_only() -> None:
    """Enable only the number platform."""
    with patch(
        "smarthub.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.NUMBER],
    ):
        yield


async def test_exclude_attributes(recorder_mock: Recorder, hass: SmartHub) -> None:
    """Test number registered attributes to be excluded."""
    assert await async_setup_component(hass, "smarthub", {})
    await async_setup_component(
        hass, number.DOMAIN, {number.DOMAIN: {"platform": "demo"}}
    )
    await hass.async_block_till_done()
    now = dt_util.utcnow()
    async_fire_time_changed(hass, now + timedelta(minutes=5))
    await hass.async_block_till_done()
    await async_wait_recording_done(hass)

    states = await hass.async_add_executor_job(
        get_significant_states, hass, now, None, hass.states.async_entity_ids()
    )
    assert len(states) > 1
    for entity_states in states.values():
        for state in entity_states:
            assert ATTR_MIN not in state.attributes
            assert ATTR_MAX not in state.attributes
            assert ATTR_STEP not in state.attributes
            assert ATTR_MODE not in state.attributes
            assert ATTR_FRIENDLY_NAME in state.attributes
