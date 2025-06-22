"""Provide a mock package component."""

import asyncio

from smarthub.core import SmartHub
from smarthub.helpers.typing import ConfigType


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Mock a successful setup."""
    asyncio.current_task().cancel()
    await asyncio.sleep(0)
