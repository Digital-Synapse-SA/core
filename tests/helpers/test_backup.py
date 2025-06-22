"""The tests for the backup helpers."""

import asyncio
from unittest.mock import patch

import pytest

from smarthub.components.backup import DOMAIN as BACKUP_DOMAIN
from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError
from smarthub.helpers import backup as backup_helper
from smarthub.setup import async_setup_component


async def test_async_get_manager(hass: SmartHub) -> None:
    """Test async_get_manager."""
    backup_helper.async_initialize_backup(hass)
    task = asyncio.create_task(backup_helper.async_get_manager(hass))
    assert await async_setup_component(hass, BACKUP_DOMAIN, {})
    await hass.async_block_till_done()
    manager = await task
    assert manager is hass.data[backup_helper.DATA_MANAGER]


async def test_async_get_manager_no_backup(hass: SmartHub) -> None:
    """Test async_get_manager when the backup integration is not enabled."""
    with pytest.raises(SmartHubError, match="Backup integration is not available"):
        await backup_helper.async_get_manager(hass)


async def test_async_get_manager_backup_failed_setup(hass: SmartHub) -> None:
    """Test test_async_get_manager when the backup integration can't be set up."""
    backup_helper.async_initialize_backup(hass)

    with patch(
        "smarthub.components.backup.manager.BackupManager.async_setup",
        side_effect=Exception("Boom!"),
    ):
        assert not await async_setup_component(hass, BACKUP_DOMAIN, {})
    with pytest.raises(Exception, match="Boom!"):
        await backup_helper.async_get_manager(hass)
