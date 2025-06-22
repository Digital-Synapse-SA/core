"""The tests for text recorder."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

import pytest

from smarthub.components import text
from smarthub.components.recorder import Recorder
from smarthub.components.recorder.history import get_significant_states
from smarthub.components.text import ATTR_MAX, ATTR_MIN, ATTR_MODE, ATTR_PATTERN
from smarthub.const import ATTR_FRIENDLY_NAME, Platform
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component
from smarthub.util import dt as dt_util

from tests.common import async_fire_time_changed
from tests.components.recorder.common import async_wait_recording_done


@pytest.fixture(autouse=True)
async def text_only() -> None:
    """Enable only the text platform."""
    with patch(
        "smarthub.components.demo.COMPONENTS_WITH_CONFIG_ENTRY_DEMO_PLATFORM",
        [Platform.TEXT],
    ):
        yield


async def test_exclude_attributes(recorder_mock: Recorder, hass: SmartHub) -> None:
    """Test siren registered attributes to be excluded."""
    now = dt_util.utcnow()
    assert await async_setup_component(hass, "smarthub", {})
    await async_setup_component(hass, text.DOMAIN, {text.DOMAIN: {"platform": "demo"}})
    await hass.async_block_till_done()
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(minutes=5))
    await hass.async_block_till_done()
    await async_wait_recording_done(hass)

    states = await hass.async_add_executor_job(
        get_significant_states, hass, now, None, hass.states.async_entity_ids()
    )
    assert len(states) >= 1
    for entity_states in states.values():
        for state in entity_states:
            for attr in (ATTR_MAX, ATTR_MIN, ATTR_MODE, ATTR_PATTERN):
                assert attr not in state.attributes
            assert ATTR_FRIENDLY_NAME in state.attributes
