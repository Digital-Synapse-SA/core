"""Describe smarthub logbook events."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from smarthub.components.logbook import (
    LOGBOOK_ENTRY_ICON,
    LOGBOOK_ENTRY_MESSAGE,
    LOGBOOK_ENTRY_NAME,
)
from smarthub.const import EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP
from smarthub.core import Event, SmartHub, callback
from smarthub.helpers.typing import NoEventData
from smarthub.util.event_type import EventType

from .const import DOMAIN

EVENT_TO_NAME: dict[EventType[Any] | str, str] = {
    EVENT_HOMEASSISTANT_STOP: "stopped",
    EVENT_HOMEASSISTANT_START: "started",
}


@callback
def async_describe_events(
    hass: SmartHub,
    async_describe_event: Callable[
        [str, EventType[NoEventData] | str, Callable[[Event], dict[str, str]]], None
    ],
) -> None:
    """Describe logbook events."""

    @callback
    def async_describe_hass_event(event: Event[NoEventData]) -> dict[str, str]:
        """Describe smarthub logbook event."""
        return {
            LOGBOOK_ENTRY_NAME: "SmartHub",
            LOGBOOK_ENTRY_MESSAGE: EVENT_TO_NAME[event.event_type],
            LOGBOOK_ENTRY_ICON: "mdi:smart-hub",
        }

    async_describe_event(DOMAIN, EVENT_HOMEASSISTANT_STOP, async_describe_hass_event)
    async_describe_event(DOMAIN, EVENT_HOMEASSISTANT_START, async_describe_hass_event)
