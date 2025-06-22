"""Define tests for the GeoJSON Events config flow."""

import pytest

from smarthub import config_entries
from smarthub.components.geo_json_events.const import DOMAIN
from smarthub.const import (
    CONF_LATITUDE,
    CONF_LOCATION,
    CONF_LONGITUDE,
    CONF_RADIUS,
    CONF_URL,
)
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

from .conftest import URL

from tests.common import MockConfigEntry

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


async def test_duplicate_error_user(
    hass: SmartHub, config_entry: MockConfigEntry
) -> None:
    """Test that errors are shown when duplicates are added."""
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["step_id"] == "user"
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_URL: URL,
            CONF_LOCATION: {
                CONF_LATITUDE: -41.2,
                CONF_LONGITUDE: 174.7,
                CONF_RADIUS: 25.0,
            },
        },
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_step_user(hass: SmartHub) -> None:
    """Test that the user step works."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["step_id"] == "user"
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_URL: URL,
            CONF_LOCATION: {
                CONF_LATITUDE: -41.2,
                CONF_LONGITUDE: 174.7,
                CONF_RADIUS: 25000.0,
            },
        },
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert (
        result["title"] == "http://geo.json.local/geo_json_events.json (-41.2, 174.7)"
    )
    assert result["data"] == {
        CONF_URL: URL,
        CONF_LATITUDE: -41.2,
        CONF_LONGITUDE: 174.7,
        CONF_RADIUS: 25.0,
    }
