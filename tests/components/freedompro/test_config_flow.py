"""Define tests for the Freedompro config flow."""

from unittest.mock import patch

import pytest

from smarthub.components.freedompro.const import DOMAIN
from smarthub.config_entries import SOURCE_USER
from smarthub.const import CONF_API_KEY
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from .const import DEVICES

VALID_CONFIG = {
    CONF_API_KEY: "ksdjfgslkjdfksjdfksjgfksjd",
}

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


async def test_show_form(hass: SmartHub) -> None:
    """Test that the form is served with no input."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"


async def test_invalid_auth(hass: SmartHub) -> None:
    """Test that errors are shown when API key is invalid."""
    with patch(
        "smarthub.components.freedompro.config_flow.get_list",
        return_value={
            "state": False,
            "code": -201,
        },
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data=VALID_CONFIG,
        )

        assert result["errors"] == {"base": "invalid_auth"}


async def test_connection_error(hass: SmartHub) -> None:
    """Test that errors are shown when API key is invalid."""
    with patch(
        "smarthub.components.freedompro.config_flow.get_list",
        return_value={
            "state": False,
            "code": -200,
        },
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data=VALID_CONFIG,
        )

        assert result["errors"] == {"base": "cannot_connect"}


async def test_create_entry(hass: SmartHub) -> None:
    """Test that the user step works."""
    with patch(
        "smarthub.components.freedompro.config_flow.get_list",
        return_value={
            "state": True,
            "devices": DEVICES,
        },
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_USER},
            data=VALID_CONFIG,
        )

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == "Freedompro"
        assert result["data"][CONF_API_KEY] == "ksdjfgslkjdfksjdfksjgfksjd"
