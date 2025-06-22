"""Backup platform for the NEW_NAME integration."""

from smarthub.core import SmartHub


async def async_pre_backup(hass: SmartHub) -> None:
    """Perform operations before a backup starts."""


async def async_post_backup(hass: SmartHub) -> None:
    """Perform operations after a backup finishes."""
