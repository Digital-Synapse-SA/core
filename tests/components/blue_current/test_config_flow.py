"""Test the Blue Current config flow."""

from unittest.mock import patch

import pytest

from smarthub import config_entries
from smarthub.components.blue_current import DOMAIN
from smarthub.components.blue_current.config_flow import (
    AlreadyConnected,
    InvalidApiToken,
    RequestLimitReached,
    WebsocketError,
)
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry


async def test_form(hass: SmartHub) -> None:
    """Test if the form is created."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["errors"] == {}
    assert result["type"] is FlowResultType.FORM


async def test_user(hass: SmartHub) -> None:
    """Test if the api token is set."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["errors"] == {}
    assert result["type"] is FlowResultType.FORM

    with (
        patch(
            "smarthub.components.blue_current.config_flow.Client.validate_api_token",
            return_value="1234",
        ),
        patch(
            "smarthub.components.blue_current.config_flow.Client.get_email",
            return_value="test@email.com",
        ),
        patch(
            "smarthub.components.blue_current.async_setup_entry",
            return_value=True,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "api_token": "123",
            },
        )
        await hass.async_block_till_done()

    assert result2["title"] == "test@email.com"
    assert result2["data"] == {"api_token": "123"}
    assert result2["type"] is FlowResultType.CREATE_ENTRY


@pytest.mark.parametrize(
    ("error", "message"),
    [
        (InvalidApiToken(), "invalid_token"),
        (RequestLimitReached(), "limit_reached"),
        (AlreadyConnected(), "already_connected"),
        (Exception(), "unknown"),
        (WebsocketError(), "cannot_connect"),
    ],
)
async def test_flow_fails(hass: SmartHub, error: Exception, message: str) -> None:
    """Test bluecurrent api errors during configuration flow."""
    with patch(
        "smarthub.components.blue_current.config_flow.Client.validate_api_token",
        side_effect=error,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
            data={"api_token": "123"},
        )
        assert result["errors"]["base"] == message
        assert result["type"] is FlowResultType.FORM

    with (
        patch(
            "smarthub.components.blue_current.config_flow.Client.validate_api_token",
            return_value="1234",
        ),
        patch(
            "smarthub.components.blue_current.config_flow.Client.get_email",
            return_value="test@email.com",
        ),
        patch(
            "smarthub.components.blue_current.async_setup_entry",
            return_value=True,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "api_token": "123",
            },
        )
        await hass.async_block_till_done()

        assert result2["title"] == "test@email.com"
        assert result2["data"] == {"api_token": "123"}
        assert result2["type"] is FlowResultType.CREATE_ENTRY


@pytest.mark.parametrize(
    ("customer_id", "reason", "expected_api_token"),
    [
        ("1234", "reauth_successful", "1234567890"),
        ("6666", "wrong_account", "123"),
    ],
)
async def test_reauth(
    hass: SmartHub,
    config_entry: MockConfigEntry,
    customer_id: str,
    reason: str,
    expected_api_token: str,
) -> None:
    """Test reauth flow."""
    config_entry.add_to_hass(hass)
    result = await config_entry.start_reauth_flow(hass)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with (
        patch(
            "smarthub.components.blue_current.config_flow.Client.validate_api_token",
            return_value=customer_id,
        ),
        patch(
            "smarthub.components.blue_current.config_flow.Client.get_email",
            return_value="test@email.com",
        ),
        patch(
            "smarthub.components.blue_current.config_flow.Client.wait_for_charge_points",
        ),
        patch(
            "smarthub.components.blue_current.Client.connect",
            lambda self, on_data, on_open: hass.loop.create_future(),
        ),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={"api_token": "1234567890"},
        )
        assert result["type"] is FlowResultType.ABORT
        assert result["reason"] == reason
        assert config_entry.data["api_token"] == expected_api_token

        await hass.async_block_till_done()
