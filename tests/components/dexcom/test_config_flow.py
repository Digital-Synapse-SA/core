"""Test the Dexcom config flow."""

from unittest.mock import patch

from pydexcom import AccountError, SessionError

from smarthub import config_entries
from smarthub.components.dexcom.const import DOMAIN
from smarthub.const import CONF_USERNAME
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from . import CONFIG


async def test_form(hass: SmartHub) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with (
        patch(
            "smarthub.components.dexcom.config_flow.Dexcom.create_session",
            return_value="test_session_id",
        ),
        patch(
            "smarthub.components.dexcom.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            CONFIG,
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == CONFIG[CONF_USERNAME]
    assert result2["data"] == CONFIG
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_account_error(hass: SmartHub) -> None:
    """Test we handle account error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "smarthub.components.dexcom.config_flow.Dexcom",
        side_effect=AccountError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            CONFIG,
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_form_session_error(hass: SmartHub) -> None:
    """Test we handle session error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "smarthub.components.dexcom.config_flow.Dexcom",
        side_effect=SessionError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            CONFIG,
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_unknown_error(hass: SmartHub) -> None:
    """Test we handle unknown error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "smarthub.components.dexcom.config_flow.Dexcom",
        side_effect=Exception,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            CONFIG,
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}
