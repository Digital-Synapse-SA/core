"""Demo platform that has two fake alarm control panels."""

from __future__ import annotations

import datetime

from smarthub.components.alarm_control_panel import AlarmControlPanelState
from smarthub.components.manual.alarm_control_panel import ManualAlarm
from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_ARMING_TIME, CONF_DELAY_TIME, CONF_TRIGGER_TIME
from smarthub.core import SmartHub
from smarthub.helpers.entity_platform import AddConfigEntryEntitiesCallback


async def async_setup_entry(
    hass: SmartHub,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Demo config entry."""
    async_add_entities(
        [
            ManualAlarm(
                hass,
                "Security",
                "demo_alarm_control_panel",
                "1234",
                None,
                True,
                False,
                {
                    AlarmControlPanelState.ARMED_AWAY: {
                        CONF_ARMING_TIME: datetime.timedelta(seconds=5),
                        CONF_DELAY_TIME: datetime.timedelta(seconds=0),
                        CONF_TRIGGER_TIME: datetime.timedelta(seconds=10),
                    },
                    AlarmControlPanelState.ARMED_HOME: {
                        CONF_ARMING_TIME: datetime.timedelta(seconds=5),
                        CONF_DELAY_TIME: datetime.timedelta(seconds=0),
                        CONF_TRIGGER_TIME: datetime.timedelta(seconds=10),
                    },
                    AlarmControlPanelState.ARMED_NIGHT: {
                        CONF_ARMING_TIME: datetime.timedelta(seconds=5),
                        CONF_DELAY_TIME: datetime.timedelta(seconds=0),
                        CONF_TRIGGER_TIME: datetime.timedelta(seconds=10),
                    },
                    AlarmControlPanelState.ARMED_VACATION: {
                        CONF_ARMING_TIME: datetime.timedelta(seconds=5),
                        CONF_DELAY_TIME: datetime.timedelta(seconds=0),
                        CONF_TRIGGER_TIME: datetime.timedelta(seconds=10),
                    },
                    AlarmControlPanelState.DISARMED: {
                        CONF_DELAY_TIME: datetime.timedelta(seconds=0),
                        CONF_TRIGGER_TIME: datetime.timedelta(seconds=10),
                    },
                    AlarmControlPanelState.ARMED_CUSTOM_BYPASS: {
                        CONF_ARMING_TIME: datetime.timedelta(seconds=5),
                        CONF_DELAY_TIME: datetime.timedelta(seconds=0),
                        CONF_TRIGGER_TIME: datetime.timedelta(seconds=10),
                    },
                    AlarmControlPanelState.TRIGGERED: {
                        CONF_ARMING_TIME: datetime.timedelta(seconds=5)
                    },
                },
            )
        ]
    )
