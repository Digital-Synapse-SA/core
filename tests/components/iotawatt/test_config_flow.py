"""Test the IoTawatt config flow."""

from unittest.mock import patch

import httpx

from smarthub import config_entries
from smarthub.components.iotawatt.const import DOMAIN
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType


async def test_form(hass: SmartHub) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == config_entries.SOURCE_USER

    with (
        patch(
            "smarthub.components.iotawatt.async_setup_entry",
            return_value=True,
        ),
        patch(
            "smarthub.components.iotawatt.config_flow.Iotawatt.connect",
            return_value=True,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "host": "1.1.1.1",
            },
        )
        await hass.async_block_till_done()

    assert len(mock_setup_entry.mock_calls) == 1
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["data"] == {
        "host": "1.1.1.1",
    }


async def test_form_auth(hass: SmartHub) -> None:
    """Test we handle auth."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch(
        "smarthub.components.iotawatt.config_flow.Iotawatt.connect",
        return_value=False,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"host": "1.1.1.1"},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == "auth"

    with patch(
        "smarthub.components.iotawatt.config_flow.Iotawatt.connect",
        return_value=False,
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "mock-user",
                "password": "mock-pass",
            },
        )
        await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.FORM
    assert result3["step_id"] == "auth"
    assert result3["errors"] == {"base": "invalid_auth"}

    with (
        patch(
            "smarthub.components.iotawatt.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
        patch(
            "smarthub.components.iotawatt.config_flow.Iotawatt.connect",
            return_value=True,
        ),
    ):
        result4 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "mock-user",
                "password": "mock-pass",
            },
        )
        await hass.async_block_till_done()

    assert result4["type"] is FlowResultType.CREATE_ENTRY
    assert len(mock_setup_entry.mock_calls) == 1
    assert result4["data"] == {
        "host": "1.1.1.1",
        "username": "mock-user",
        "password": "mock-pass",
    }


async def test_form_cannot_connect(hass: SmartHub) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "smarthub.components.iotawatt.config_flow.Iotawatt.connect",
        side_effect=httpx.HTTPError("any"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"host": "1.1.1.1"},
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_setup_exception(hass: SmartHub) -> None:
    """Test we handle broad exception."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "smarthub.components.iotawatt.config_flow.Iotawatt.connect",
        side_effect=Exception,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"host": "1.1.1.1"},
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}
