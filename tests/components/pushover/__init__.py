"""Tests for the pushover component."""

from smarthub.components.pushover.const import CONF_USER_KEY
from smarthub.const import CONF_API_KEY, CONF_NAME

MOCK_CONFIG = {
    CONF_NAME: "Pushover",
    CONF_API_KEY: "MYAPIKEY",
    CONF_USER_KEY: "MYUSERKEY",
}
