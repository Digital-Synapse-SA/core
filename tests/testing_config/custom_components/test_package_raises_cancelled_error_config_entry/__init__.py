"""Provide a mock package component."""

import asyncio

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.helpers.typing import ConfigType


async def async_setup(hass: SmartHub, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True


async def async_setup_entry(hass: SmartHub, entry: ConfigEntry) -> None:
    """Mock an unsuccessful entry setup."""
    asyncio.current_task().cancel()
    await asyncio.sleep(0)
