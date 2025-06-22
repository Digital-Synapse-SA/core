"""Tests for the Trafikverket Ferry integration."""

from __future__ import annotations

from smarthub.components.trafikverket_ferry.const import (
    CONF_FROM,
    CONF_TIME,
    CONF_TO,
)
from smarthub.const import CONF_API_KEY, CONF_NAME, CONF_WEEKDAY, WEEKDAYS

ENTRY_CONFIG = {
    CONF_API_KEY: "1234567890",
    CONF_FROM: "Harbor 1",
    CONF_TO: "Harbor 2",
    CONF_TIME: "00:00:00",
    CONF_WEEKDAY: WEEKDAYS,
    CONF_NAME: "Harbor1",
}
