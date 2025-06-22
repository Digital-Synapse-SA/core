"""Constants for the SmartHub alerts integration."""

from datetime import timedelta

import aiohttp

COMPONENT_LOADED_COOLDOWN = 30
DOMAIN = "smarthub_alerts"
UPDATE_INTERVAL = timedelta(hours=3)

REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=30)
