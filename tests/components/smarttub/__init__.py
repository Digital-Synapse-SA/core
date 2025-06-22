"""Tests for the smarttub integration."""

from datetime import timedelta

from smarthub.components.smarttub.const import SCAN_INTERVAL
from smarthub.core import SmartHub
from smarthub.util import dt as dt_util

from tests.common import async_fire_time_changed


async def trigger_update(hass: SmartHub) -> None:
    """Trigger a polling update by moving time forward."""
    new_time = dt_util.utcnow() + timedelta(seconds=SCAN_INTERVAL + 1)
    async_fire_time_changed(hass, new_time)
    await hass.async_block_till_done(wait_background_tasks=True)
