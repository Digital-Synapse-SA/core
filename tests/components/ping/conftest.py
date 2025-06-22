"""Test configuration for ping."""

from unittest.mock import patch

from icmplib import Host
import pytest

from smarthub.components.device_tracker import CONF_CONSIDER_HOME
from smarthub.components.ping import CONF_PING_COUNT, DOMAIN
from smarthub.const import CONF_HOST
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


@pytest.fixture
def patch_setup(*args, **kwargs):
    """Patch setup methods."""
    with (
        patch(
            "smarthub.components.ping.async_setup_entry",
            return_value=True,
        ),
        patch("smarthub.components.ping.async_setup", return_value=True),
    ):
        yield


@pytest.fixture(autouse=True)
async def patch_ping():
    """Patch icmplib async_ping."""
    mock = Host("10.10.10.10", 5, [10, 1, 2, 5, 6])

    with (
        patch("smarthub.components.ping.helpers.async_ping", return_value=mock),
        patch("smarthub.components.ping.async_ping", return_value=mock),
    ):
        yield mock


@pytest.fixture(name="config_entry")
async def mock_config_entry(hass: SmartHub) -> MockConfigEntry:
    """Return a MockConfigEntry for testing."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="10.10.10.10",
        options={
            CONF_HOST: "10.10.10.10",
            CONF_PING_COUNT: 10.0,
            CONF_CONSIDER_HOME: 180,
        },
    )


@pytest.fixture(name="setup_integration")
async def mock_setup_integration(
    hass: SmartHub, config_entry: MockConfigEntry, patch_ping
) -> None:
    """Fixture for setting up the component."""
    config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
