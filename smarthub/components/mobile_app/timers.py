"""Timers for the mobile app."""

from datetime import timedelta

from smarthub.components import notify
from smarthub.components.intent import TimerEventType, TimerInfo
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_DEVICE_ID
from smarthub.core import SmartHub, callback

from . import device_action


@callback
def async_handle_timer_event(
    hass: SmartHub,
    entry: ConfigEntry,
    event_type: TimerEventType,
    timer_info: TimerInfo,
) -> None:
    """Handle timer events."""
    if event_type != TimerEventType.FINISHED:
        return

    if timer_info.name:
        message = f"{timer_info.name} finished"
    else:
        message = f"{timedelta(seconds=timer_info.created_seconds)} timer finished"

    entry.async_create_task(
        hass,
        device_action.async_call_action_from_config(
            hass,
            {
                CONF_DEVICE_ID: timer_info.device_id,
                notify.ATTR_MESSAGE: message,
                notify.ATTR_DATA: {
                    "group": "timers",
                    # Android
                    "channel": "Timers",
                    "importance": "high",
                    "ttl": 0,
                    "priority": "high",
                    # iOS
                    "push": {
                        "interruption-level": "time-sensitive",
                    },
                },
            },
            {},
            None,
        ),
        "mobile_app_timer_notification",
    )
