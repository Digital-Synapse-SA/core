"""Test the Firmata config flow."""

from unittest.mock import patch

from pymata_express.pymata_express_serial import serial

from smarthub import config_entries
from smarthub.components.firmata.const import CONF_SERIAL_PORT, DOMAIN
from smarthub.const import CONF_NAME
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType


async def test_import_cannot_connect_pymata(hass: SmartHub) -> None:
    """Test we fail with an invalid board."""

    with patch(
        "smarthub.components.firmata.board.PymataExpress.start_aio",
        side_effect=RuntimeError,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_IMPORT},
            data={CONF_SERIAL_PORT: "/dev/nonExistent"},
        )

        assert result["type"] is FlowResultType.ABORT
        assert result["reason"] == "cannot_connect"


async def test_import_cannot_connect_serial(hass: SmartHub) -> None:
    """Test we fail with an invalid board."""

    with patch(
        "smarthub.components.firmata.board.PymataExpress.start_aio",
        side_effect=serial.SerialException,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_IMPORT},
            data={CONF_SERIAL_PORT: "/dev/nonExistent"},
        )

        assert result["type"] is FlowResultType.ABORT
        assert result["reason"] == "cannot_connect"


async def test_import_cannot_connect_serial_timeout(hass: SmartHub) -> None:
    """Test we fail with an invalid board."""

    with patch(
        "smarthub.components.firmata.board.PymataExpress.start_aio",
        side_effect=serial.SerialTimeoutException,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_IMPORT},
            data={CONF_SERIAL_PORT: "/dev/nonExistent"},
        )

        assert result["type"] is FlowResultType.ABORT
        assert result["reason"] == "cannot_connect"


async def test_import(hass: SmartHub) -> None:
    """Test we create an entry from config."""

    with (
        patch("smarthub.components.firmata.board.PymataExpress", autospec=True),
        patch(
            "smarthub.components.firmata.async_setup", return_value=True
        ) as mock_setup,
        patch(
            "smarthub.components.firmata.async_setup_entry", return_value=True
        ) as mock_setup_entry,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_IMPORT},
            data={CONF_SERIAL_PORT: "/dev/nonExistent"},
        )

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == "serial-/dev/nonExistent"
        assert result["data"] == {
            CONF_NAME: "serial-/dev/nonExistent",
            CONF_SERIAL_PORT: "/dev/nonExistent",
        }
        await hass.async_block_till_done()
        assert len(mock_setup.mock_calls) == 1
        assert len(mock_setup_entry.mock_calls) == 1
