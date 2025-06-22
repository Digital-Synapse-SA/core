"""Ecovacs test util."""

import asyncio

from deebot_client.event_bus import EventBus
from deebot_client.events import Event

from smarthub.core import SmartHub


async def block_till_done(hass: SmartHub, event_bus: EventBus) -> None:
    """Block till done."""
    await asyncio.gather(*event_bus._tasks)
    await hass.async_block_till_done()


async def notify_and_wait(
    hass: SmartHub, event_bus: EventBus, event: Event
) -> None:
    """Block till done."""
    event_bus.notify(event)
    await block_till_done(hass, event_bus)
