"""Test the baf init flow."""

from unittest.mock import patch

from aiobafi6.exceptions import DeviceUUIDMismatchError
import pytest

from smarthub.components.baf.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.const import CONF_IP_ADDRESS
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from . import MOCK_UUID, MockBAFDevice

from tests.common import MockConfigEntry


def _patch_device_init(side_effect=None):
    """Mock out the BAF Device object."""

    def _create_mock_baf(*args, **kwargs):
        return MockBAFDevice(side_effect)

    return patch("smarthub.components.baf.Device", _create_mock_baf)


async def test_config_entry_wrong_uuid(
    hass: SmartHub, caplog: pytest.LogCaptureFixture
) -> None:
    """Test config entry enters setup retry when uuid mismatches."""
    mismatched_uuid = MOCK_UUID + "0"
    already_migrated_config_entry = MockConfigEntry(
        domain=DOMAIN, data={CONF_IP_ADDRESS: "127.0.0.1"}, unique_id=mismatched_uuid
    )
    already_migrated_config_entry.add_to_hass(hass)
    with _patch_device_init(DeviceUUIDMismatchError):
        await async_setup_component(hass, DOMAIN, {DOMAIN: {}})
        await hass.async_block_till_done()
    assert already_migrated_config_entry.state is ConfigEntryState.SETUP_RETRY
    assert (
        "Unexpected device found at 127.0.0.1; expected 12340, found 1234"
        in caplog.text
    )
