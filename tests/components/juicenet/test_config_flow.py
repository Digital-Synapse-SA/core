"""Test the JuiceNet config flow."""

from unittest.mock import MagicMock, patch

import aiohttp
from pyjuicenet import TokenError

from smarthub import config_entries
from smarthub.components.juicenet.const import DOMAIN
from smarthub.const import CONF_ACCESS_TOKEN
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType


def _mock_juicenet_return_value(get_devices=None):
    juicenet_mock = MagicMock()
    type(juicenet_mock).get_devices = MagicMock(return_value=get_devices)
    return juicenet_mock


async def test_form(hass: SmartHub) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with (
        patch(
            "smarthub.components.juicenet.config_flow.Api.get_devices",
            return_value=MagicMock(),
        ),
        patch(
            "smarthub.components.juicenet.async_setup", return_value=True
        ) as mock_setup,
        patch(
            "smarthub.components.juicenet.async_setup_entry", return_value=True
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ACCESS_TOKEN: "access_token"}
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "JuiceNet"
    assert result2["data"] == {CONF_ACCESS_TOKEN: "access_token"}
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(hass: SmartHub) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "smarthub.components.juicenet.config_flow.Api.get_devices",
        side_effect=TokenError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ACCESS_TOKEN: "access_token"}
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_form_cannot_connect(hass: SmartHub) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "smarthub.components.juicenet.config_flow.Api.get_devices",
        side_effect=aiohttp.ClientError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ACCESS_TOKEN: "access_token"}
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_catch_unknown_errors(hass: SmartHub) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "smarthub.components.juicenet.config_flow.Api.get_devices",
        side_effect=Exception,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_ACCESS_TOKEN: "access_token"}
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}


async def test_import(hass: SmartHub) -> None:
    """Test that import works as expected."""

    with (
        patch(
            "smarthub.components.juicenet.config_flow.Api.get_devices",
            return_value=MagicMock(),
        ),
        patch(
            "smarthub.components.juicenet.async_setup", return_value=True
        ) as mock_setup,
        patch(
            "smarthub.components.juicenet.async_setup_entry", return_value=True
        ) as mock_setup_entry,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_IMPORT},
            data={CONF_ACCESS_TOKEN: "access_token"},
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "JuiceNet"
    assert result["data"] == {CONF_ACCESS_TOKEN: "access_token"}
    assert len(mock_setup.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1
