"""Tests for the Econet component."""

from unittest.mock import patch

from pyeconet.api import EcoNetApiInterface
from pyeconet.errors import InvalidCredentialsError, PyeconetError

from smarthub.components.econet.const import DOMAIN
from smarthub.config_entries import SOURCE_USER
from smarthub.const import CONF_EMAIL, CONF_PASSWORD
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry


async def test_bad_credentials(hass: SmartHub) -> None:
    """Test when provided credentials are rejected."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with (
        patch(
            "pyeconet.EcoNetApiInterface.login",
            side_effect=InvalidCredentialsError(),
        ),
        patch("smarthub.components.econet.async_setup_entry", return_value=True),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: "admin@localhost.com",
                CONF_PASSWORD: "password0",
            },
        )

        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"
        assert result["errors"] == {
            "base": "invalid_auth",
        }


async def test_generic_error_from_library(hass: SmartHub) -> None:
    """Test when connection fails."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with (
        patch(
            "pyeconet.EcoNetApiInterface.login",
            side_effect=PyeconetError(),
        ),
        patch("smarthub.components.econet.async_setup_entry", return_value=True),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: "admin@localhost.com",
                CONF_PASSWORD: "password0",
            },
        )

        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"
        assert result["errors"] == {
            "base": "cannot_connect",
        }


async def test_auth_worked(hass: SmartHub) -> None:
    """Test when provided credentials are accepted."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with (
        patch(
            "pyeconet.EcoNetApiInterface.login",
            return_value=EcoNetApiInterface,
        ),
        patch("smarthub.components.econet.async_setup_entry", return_value=True),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: "admin@localhost.com",
                CONF_PASSWORD: "password0",
            },
        )

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["data"] == {
            CONF_EMAIL: "admin@localhost.com",
            CONF_PASSWORD: "password0",
        }


async def test_already_configured(hass: SmartHub) -> None:
    """Test when provided credentials are already configured."""
    config = {
        CONF_EMAIL: "admin@localhost.com",
        CONF_PASSWORD: "password0",
    }
    MockConfigEntry(
        domain=DOMAIN, data=config, unique_id="admin@localhost.com"
    ).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with (
        patch(
            "pyeconet.EcoNetApiInterface.login",
            return_value=EcoNetApiInterface,
        ),
        patch("smarthub.components.econet.async_setup_entry", return_value=True),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={
                CONF_EMAIL: "admin@localhost.com",
                CONF_PASSWORD: "password0",
            },
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
