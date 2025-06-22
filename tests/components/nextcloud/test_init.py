"""Tests for the Nextcloud init."""

from unittest.mock import Mock, patch

from nextcloudmonitor import (
    NextcloudMonitorAuthorizationError,
    NextcloudMonitorConnectionError,
    NextcloudMonitorError,
    NextcloudMonitorRequestError,
)
import pytest

from smarthub.components.nextcloud.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.const import CONF_URL, Platform
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from . import init_integration, mock_config_entry
from .const import MOCKED_ENTRY_ID, NC_DATA, VALID_CONFIG


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_async_setup_entry(
    hass: SmartHub,
) -> None:
    """Test a successful setup entry."""
    assert await init_integration(hass, VALID_CONFIG, NC_DATA)


async def test_unique_id_migration(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test migration of unique ids to stable ones."""

    object_id = "my_nc_url_local_system_version"
    entity_id = f"{Platform.SENSOR}.{object_id}"

    entry = mock_config_entry(VALID_CONFIG)
    entry.add_to_hass(hass)

    entity = entity_registry.async_get_or_create(
        Platform.SENSOR,
        DOMAIN,
        f"{VALID_CONFIG[CONF_URL]}#nextcloud_system_version",
        suggested_object_id=object_id,
        config_entry=entry,
    )

    # test old unique id
    assert entity.entity_id == entity_id
    assert entity.unique_id == f"{VALID_CONFIG[CONF_URL]}#nextcloud_system_version"

    with (
        patch(
            "smarthub.components.nextcloud.NextcloudMonitor"
        ) as mock_nextcloud_monitor,
    ):
        mock_nextcloud_monitor.update = Mock(return_value=True)
        mock_nextcloud_monitor.return_value.data = NC_DATA
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    # test migrated unique id
    reg_entry = entity_registry.async_get(entity_id)
    assert reg_entry.unique_id == f"{MOCKED_ENTRY_ID}#system_version"


@pytest.mark.parametrize(
    ("exception", "expcted_entry_state"),
    [
        (NextcloudMonitorAuthorizationError, ConfigEntryState.SETUP_ERROR),
        (NextcloudMonitorConnectionError, ConfigEntryState.SETUP_RETRY),
        (NextcloudMonitorRequestError, ConfigEntryState.SETUP_RETRY),
    ],
)
async def test_setup_entry_errors(
    hass: SmartHub,
    exception: NextcloudMonitorError,
    expcted_entry_state: ConfigEntryState,
) -> None:
    """Test a successful setup entry."""

    entry = mock_config_entry(VALID_CONFIG)
    entry.add_to_hass(hass)

    with (
        patch(
            "smarthub.components.nextcloud.NextcloudMonitor", side_effect=exception
        ),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        assert entry.state == expcted_entry_state
