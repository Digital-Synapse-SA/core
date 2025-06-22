"""The tests for group recorder."""

from __future__ import annotations

from datetime import timedelta

import pytest

from smarthub.components import group
from smarthub.components.group import ATTR_AUTO, ATTR_ENTITY_ID, ATTR_ORDER
from smarthub.components.recorder import Recorder
from smarthub.components.recorder.history import get_significant_states
from smarthub.const import ATTR_FRIENDLY_NAME, STATE_ON
from smarthub.core import SmartHub, split_entity_id
from smarthub.setup import async_setup_component
from smarthub.util import dt as dt_util

from tests.common import async_fire_time_changed
from tests.components.recorder.common import async_wait_recording_done


@pytest.fixture(autouse=True)
async def setup_smarthub():
    """Override the fixture in group.conftest."""


async def test_exclude_attributes(recorder_mock: Recorder, hass: SmartHub) -> None:
    """Test number registered attributes to be excluded."""
    now = dt_util.utcnow()
    hass.states.async_set("light.bowl", STATE_ON)

    assert await async_setup_component(hass, "light", {})
    assert await async_setup_component(
        hass,
        group.DOMAIN,
        {
            group.DOMAIN: {
                "group_zero": {"entities": "light.Bowl", "icon": "mdi:work"},
                "group_one": {"entities": "light.Bowl", "icon": "mdi:work"},
                "group_two": {"entities": "light.Bowl", "icon": "mdi:work"},
            }
        },
    )
    await hass.async_block_till_done()
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(minutes=5))
    await hass.async_block_till_done()
    await async_wait_recording_done(hass)

    states = await hass.async_add_executor_job(
        get_significant_states, hass, now, None, hass.states.async_entity_ids()
    )
    assert len(states) > 1
    for entity_states in states.values():
        for state in entity_states:
            if split_entity_id(state.entity_id)[0] == group.DOMAIN:
                assert ATTR_AUTO not in state.attributes
                assert ATTR_ENTITY_ID not in state.attributes
                assert ATTR_ORDER not in state.attributes
                assert ATTR_FRIENDLY_NAME in state.attributes
