"""Test the FireServiceRota config flow."""

from unittest.mock import patch

from pyfireservicerota import InvalidAuthError

from smarthub import config_entries
from smarthub.components.fireservicerota.const import DOMAIN
from smarthub.const import CONF_PASSWORD, CONF_URL, CONF_USERNAME
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from tests.common import MockConfigEntry

MOCK_CONF = {
    CONF_USERNAME: "my@email.address",
    CONF_PASSWORD: "mypassw0rd",
    CONF_URL: "www.brandweerrooster.nl",
}

MOCK_DATA = {
    "auth_implementation": DOMAIN,
    CONF_URL: MOCK_CONF[CONF_URL],
    CONF_USERNAME: MOCK_CONF[CONF_USERNAME],
    "token": {
        "access_token": "test-access-token",
        "token_type": "Bearer",
        "expires_in": 1234,
        "refresh_token": "test-refresh-token",
        "created_at": 4321,
    },
}

MOCK_TOKEN_INFO = {
    "access_token": "test-access-token",
    "token_type": "Bearer",
    "expires_in": 1234,
    "refresh_token": "test-refresh-token",
    "created_at": 4321,
}


async def test_show_form(hass: SmartHub) -> None:
    """Test that the form is served with no input."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"


async def test_abort_if_already_setup(hass: SmartHub) -> None:
    """Test abort if already setup."""
    entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONF, unique_id=MOCK_CONF[CONF_USERNAME]
    )
    entry.add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}, data=MOCK_CONF
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_invalid_credentials(hass: SmartHub) -> None:
    """Test that invalid credentials throws an error."""

    with patch(
        "smarthub.components.fireservicerota.coordinator.FireServiceRota.request_tokens",
        side_effect=InvalidAuthError,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}, data=MOCK_CONF
        )
        assert result["errors"] == {"base": "invalid_auth"}


async def test_step_user(hass: SmartHub) -> None:
    """Test the start of the config flow."""

    with (
        patch(
            "smarthub.components.fireservicerota.config_flow.FireServiceRota"
        ) as mock_fsr,
        patch(
            "smarthub.components.fireservicerota.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
    ):
        mock_fireservicerota = mock_fsr.return_value
        mock_fireservicerota.request_tokens.return_value = MOCK_TOKEN_INFO

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}, data=MOCK_CONF
        )

        await hass.async_block_till_done()

        assert result["type"] is FlowResultType.CREATE_ENTRY
        assert result["title"] == MOCK_CONF[CONF_USERNAME]
        assert result["data"] == {
            "auth_implementation": "fireservicerota",
            CONF_URL: "www.brandweerrooster.nl",
            CONF_USERNAME: "my@email.address",
            "token": {
                "access_token": "test-access-token",
                "token_type": "Bearer",
                "expires_in": 1234,
                "refresh_token": "test-refresh-token",
                "created_at": 4321,
            },
        }

        assert len(mock_setup_entry.mock_calls) == 1


async def test_reauth(hass: SmartHub) -> None:
    """Test the start of the config flow."""
    entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONF, unique_id=MOCK_CONF[CONF_USERNAME]
    )
    entry.add_to_hass(hass)
    result = await entry.start_reauth_flow(hass)
    assert result["type"] is FlowResultType.FORM

    with (
        patch(
            "smarthub.components.fireservicerota.config_flow.FireServiceRota"
        ) as mock_fsr,
        patch(
            "smarthub.components.fireservicerota.async_setup_entry",
            return_value=True,
        ),
    ):
        mock_fireservicerota = mock_fsr.return_value
        mock_fireservicerota.request_tokens.return_value = MOCK_TOKEN_INFO
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_PASSWORD: "any"},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.ABORT
    assert result2["reason"] == "reauth_successful"
