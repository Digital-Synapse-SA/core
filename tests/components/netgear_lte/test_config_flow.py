"""Test Netgear LTE config flow."""

from unittest.mock import patch

from smarthub.components.netgear_lte.const import DOMAIN
from smarthub.config_entries import SOURCE_USER
from smarthub.const import CONF_SOURCE
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from .conftest import CONF_DATA


def _patch_setup():
    return patch(
        "smarthub.components.netgear_lte.async_setup_entry", return_value=True
    )


async def test_flow_user_form(hass: SmartHub, connection: None) -> None:
    """Test that the user set up form is served."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={CONF_SOURCE: SOURCE_USER},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with _patch_setup():
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=CONF_DATA,
        )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Netgear LM1200"
    assert result["data"] == CONF_DATA
    assert result["context"]["unique_id"] == "FFFFFFFFFFFFF"


async def test_flow_already_configured(
    hass: SmartHub, setup_integration: None
) -> None:
    """Test config flow aborts when already configured."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={CONF_SOURCE: SOURCE_USER},
        data=CONF_DATA,
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_flow_user_cannot_connect(
    hass: SmartHub, cannot_connect: None
) -> None:
    """Test connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={CONF_SOURCE: SOURCE_USER},
        data=CONF_DATA,
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"]["base"] == "cannot_connect"


async def test_flow_user_unknown_error(hass: SmartHub, unknown: None) -> None:
    """Test unknown error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={CONF_SOURCE: SOURCE_USER},
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input=CONF_DATA,
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"]["base"] == "unknown"
