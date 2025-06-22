"""Backup platform for the Recorder integration."""

from logging import getLogger

from smarthub.core import CoreState, SmartHub
from smarthub.exceptions import SmartHubError

from .util import async_migration_in_progress, get_instance

_LOGGER = getLogger(__name__)


async def async_pre_backup(hass: SmartHub) -> None:
    """Perform operations before a backup starts."""
    _LOGGER.info("Backup start notification, locking database for writes")
    instance = get_instance(hass)
    if hass.state is not CoreState.running:
        raise SmartHubError("SmartHub is not running")
    if async_migration_in_progress(hass):
        raise SmartHubError("Database migration in progress")
    await instance.lock_database()


async def async_post_backup(hass: SmartHub) -> None:
    """Perform operations after a backup finishes."""
    instance = get_instance(hass)
    _LOGGER.info("Backup end notification, releasing write lock")
    if not instance.unlock_database():
        raise SmartHubError("Could not release database write lock")
