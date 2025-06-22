"""Constants for NuHeat thermostats."""

from smarthub.const import Platform

DOMAIN = "nuheat"

PLATFORMS = [Platform.CLIMATE]

CONF_SERIAL_NUMBER = "serial_number"

MANUFACTURER = "NuHeat"

NUHEAT_API_STATE_SHIFT_DELAY = 2
