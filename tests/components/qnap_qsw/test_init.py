"""Define tests for the QNAP QSW init."""

from unittest.mock import patch

from aioqsw.exceptions import APIError

from smarthub.components.qnap_qsw.const import DOMAIN
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from .util import CONFIG

from tests.common import MockConfigEntry


async def test_firmware_check_error(hass: SmartHub) -> None:
    """Test firmware update check error."""

    config_entry = MockConfigEntry(
        domain=DOMAIN, unique_id="qsw_unique_id", data=CONFIG
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "smarthub.components.qnap_qsw.QnapQswApi.check_firmware",
            side_effect=APIError,
        ),
        patch(
            "smarthub.components.qnap_qsw.QnapQswApi.validate",
            return_value=None,
        ),
        patch(
            "smarthub.components.qnap_qsw.QnapQswApi.update",
            return_value=None,
        ),
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert config_entry.state is ConfigEntryState.LOADED


async def test_unload_entry(hass: SmartHub) -> None:
    """Test unload."""

    config_entry = MockConfigEntry(
        domain=DOMAIN, unique_id="qsw_unique_id", data=CONFIG
    )
    config_entry.add_to_hass(hass)

    with (
        patch(
            "smarthub.components.qnap_qsw.QnapQswApi.check_firmware",
            return_value=None,
        ),
        patch(
            "smarthub.components.qnap_qsw.QnapQswApi.validate",
            return_value=None,
        ),
        patch(
            "smarthub.components.qnap_qsw.QnapQswApi.update",
            return_value=None,
        ),
    ):
        assert await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
        assert config_entry.state is ConfigEntryState.LOADED

        await hass.config_entries.async_unload(config_entry.entry_id)
        await hass.async_block_till_done()
        assert config_entry.state is ConfigEntryState.NOT_LOADED
