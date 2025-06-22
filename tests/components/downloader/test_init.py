"""Tests for the downloader component init."""

from unittest.mock import patch

from smarthub.components.downloader.const import (
    CONF_DOWNLOAD_DIR,
    DOMAIN,
    SERVICE_DOWNLOAD_FILE,
)
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


async def test_initialization(hass: SmartHub) -> None:
    """Test the initialization of the downloader component."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_DOWNLOAD_DIR: "/test_dir",
        },
    )
    config_entry.add_to_hass(hass)
    with patch("os.path.isdir", return_value=True):
        assert await hass.config_entries.async_setup(config_entry.entry_id)

    assert hass.services.has_service(DOMAIN, SERVICE_DOWNLOAD_FILE)
    assert config_entry.state is ConfigEntryState.LOADED
