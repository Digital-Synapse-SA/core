"""Z-Wave JS trigger dispatcher."""

from __future__ import annotations

from smarthub.core import SmartHub
from smarthub.helpers.trigger import Trigger

from .triggers import event, value_updated

TRIGGERS = {
    event.PLATFORM_TYPE: event.EventTrigger,
    value_updated.PLATFORM_TYPE: value_updated.ValueUpdatedTrigger,
}


async def async_get_triggers(hass: SmartHub) -> dict[str, type[Trigger]]:
    """Return the triggers for Z-Wave JS."""
    return TRIGGERS
