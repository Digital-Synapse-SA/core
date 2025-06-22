"""Constants for the CPU Speed integration."""

import logging
from typing import Final

from smarthub.const import Platform

DOMAIN: Final = "cpuspeed"
PLATFORMS = [Platform.SENSOR]

LOGGER = logging.getLogger(__package__)
