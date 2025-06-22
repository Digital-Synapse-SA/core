"""Test the FAA Delays config flow."""

from unittest.mock import patch

from aiohttp import ClientConnectionError
import faadelays

from smarthub import config_entries
from smarthub.components.faa_delays.const import DOMAIN
from smarthub.const import CONF_ID
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType
from smarthub.exceptions import SmartHubError

from tests.common import MockConfigEntry


async def mock_valid_airport(self, *args, **kwargs):
    """Return a valid airport."""
    self.code = "test"


async def test_form(hass: SmartHub) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with (
        patch.object(faadelays.Airport, "update", new=mock_valid_airport),
        patch(
            "smarthub.components.faa_delays.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "id": "test",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "test"
    assert result2["data"] == {
        "id": "test",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_duplicate_error(hass: SmartHub) -> None:
    """Test that we handle a duplicate configuration."""
    conf = {CONF_ID: "test"}

    MockConfigEntry(domain=DOMAIN, unique_id="test", data=conf).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}, data=conf
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_form_cannot_connect(hass: SmartHub) -> None:
    """Test we handle a connection error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch("faadelays.Airport.update", side_effect=ClientConnectionError):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "id": "test",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_unexpected_exception(hass: SmartHub) -> None:
    """Test we handle an unexpected exception."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch("faadelays.Airport.update", side_effect=SmartHubError):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "id": "test",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}
