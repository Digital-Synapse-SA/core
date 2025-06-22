"""Test the Brottsplatskartan config flow."""

from __future__ import annotations

import pytest

from smarthub import config_entries
from smarthub.components.brottsplatskartan.const import CONF_AREA, DOMAIN
from smarthub.const import CONF_LATITUDE, CONF_LOCATION, CONF_LONGITUDE
from smarthub.core import SmartHub
from smarthub.data_entry_flow import FlowResultType

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


async def test_form(hass: SmartHub) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {},
    )
    await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Brottsplatskartan HOME"
    assert result2["data"] == {
        "area": None,
        "latitude": hass.config.latitude,
        "longitude": hass.config.longitude,
        "app_id": "ha-1234567890",
    }


async def test_form_location(hass: SmartHub) -> None:
    """Test we get the form using location."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_LOCATION: {
                CONF_LATITUDE: 59.32,
                CONF_LONGITUDE: 18.06,
            },
        },
    )
    await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Brottsplatskartan 59.32, 18.06"
    assert result2["data"] == {
        "area": None,
        "latitude": 59.32,
        "longitude": 18.06,
        "app_id": "ha-1234567890",
    }


async def test_form_area(hass: SmartHub) -> None:
    """Test we get the form using area."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_LOCATION: {
                CONF_LATITUDE: 59.32,
                CONF_LONGITUDE: 18.06,
            },
            CONF_AREA: "Stockholms län",
        },
    )
    await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Brottsplatskartan Stockholms län"
    assert result2["data"] == {
        "latitude": None,
        "longitude": None,
        "area": "Stockholms län",
        "app_id": "ha-1234567890",
    }
