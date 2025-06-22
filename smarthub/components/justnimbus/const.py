"""Constants for the JustNimbus integration."""

from typing import Final

from smarthub.const import Platform

DOMAIN = "justnimbus"

PLATFORMS = [
    Platform.SENSOR,
]

CONF_ZIP_CODE: Final = "zip_code"
