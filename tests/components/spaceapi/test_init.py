"""The tests for the SmartHub SpaceAPI component."""

from http import HTTPStatus
from unittest.mock import patch

from aiohttp.test_utils import TestClient
import pytest

from smarthub.components.spaceapi import (
    ATTR_SENSOR_LOCATION,
    DOMAIN,
    SPACEAPI_VERSION,
    URL_API_SPACEAPI,
)
from smarthub.const import ATTR_UNIT_OF_MEASUREMENT, PERCENTAGE, UnitOfTemperature
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from tests.typing import ClientSessionGenerator

CONFIG = {
    DOMAIN: {
        "space": "Home",
        "logo": "https://smart-hub.io/logo.png",
        "url": "https://smart-hub.io",
        "location": {"address": "In your Home"},
        "contact": {"email": "hello@smart-hub.io"},
        "issue_report_channels": ["email"],
        "state": {
            "entity_id": "test.test_door",
            "icon_open": "https://smart-hub.io/open.png",
            "icon_closed": "https://smart-hub.io/close.png",
        },
        "sensors": {
            "temperature": ["test.temp1", "test.temp2", "test.temp3"],
            "humidity": ["test.hum1"],
        },
        "spacefed": {"spacenet": True, "spacesaml": False, "spacephone": True},
        "cam": ["https://smart-hub.io/cam1", "https://smart-hub.io/cam2"],
        "stream": {
            "m4": "https://smart-hub.io/m4",
            "mjpeg": "https://smart-hub.io/mjpeg",
            "ustream": "https://smart-hub.io/ustream",
        },
        "feeds": {
            "blog": {"url": "https://smart-hub.io/blog"},
            "wiki": {"type": "mediawiki", "url": "https://smart-hub.io/wiki"},
            "calendar": {"type": "ical", "url": "https://smart-hub.io/calendar"},
            "flicker": {"url": "https://www.flickr.com/photos/smart-hub"},
        },
        "cache": {"schedule": "m.02"},
        "projects": [
            "https://smart-hub.io/projects/1",
            "https://smart-hub.io/projects/2",
            "https://smart-hub.io/projects/3",
        ],
        "radio_show": [
            {
                "name": "Radioshow",
                "url": "https://smart-hub.io/radio",
                "type": "ogg",
                "start": "2019-09-02T10:00Z",
                "end": "2019-09-02T12:00Z",
            }
        ],
    }
}

SENSOR_OUTPUT = {
    "temperature": [
        {
            "location": "Home",
            "name": "temp1",
            "unit": UnitOfTemperature.CELSIUS,
            "value": 25.0,
        },
        {
            "location": "outside",
            "name": "temp2",
            "unit": UnitOfTemperature.CELSIUS,
            "value": 23.0,
        },
        {
            "location": "Home",
            "name": "temp3",
            "unit": UnitOfTemperature.CELSIUS,
            "value": None,
        },
    ],
    "humidity": [
        {"location": "Home", "name": "hum1", "unit": PERCENTAGE, "value": 88.0}
    ],
}


@pytest.fixture
async def mock_client(
    hass: SmartHub, hass_client: ClientSessionGenerator
) -> TestClient:
    """Start the SmartHub HTTP component."""
    with patch("smarthub.components.spaceapi", return_value=True):
        await async_setup_component(hass, "spaceapi", CONFIG)

    hass.states.async_set(
        "test.temp1",
        25,
        attributes={ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS},
    )
    hass.states.async_set(
        "test.temp2",
        23,
        attributes={
            ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS,
            ATTR_SENSOR_LOCATION: "outside",
        },
    )
    hass.states.async_set(
        "test.temp3",
        "foo",
        attributes={ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS},
    )
    hass.states.async_set(
        "test.temp3",
        "foo",
        attributes={ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS},
    )
    hass.states.async_set(
        "test.hum1", 88, attributes={ATTR_UNIT_OF_MEASUREMENT: PERCENTAGE}
    )

    return await hass_client()


async def test_spaceapi_get(hass: SmartHub, mock_client) -> None:
    """Test response after start-up SmartHub."""
    resp = await mock_client.get(URL_API_SPACEAPI)
    assert resp.status == HTTPStatus.OK

    data = await resp.json()

    assert data["api"] == SPACEAPI_VERSION
    assert data["space"] == "Home"
    assert data["contact"]["email"] == "hello@smart-hub.io"
    assert data["location"]["address"] == "In your Home"
    assert data["location"]["lat"] == 32.87336
    assert data["location"]["lon"] == -117.22743
    assert data["state"]["open"] == "null"
    assert data["state"]["icon"]["open"] == "https://smart-hub.io/open.png"
    assert data["state"]["icon"]["closed"] == "https://smart-hub.io/close.png"
    assert data["spacefed"]["spacenet"] == bool(1)
    assert data["spacefed"]["spacesaml"] == bool(0)
    assert data["spacefed"]["spacephone"] == bool(1)
    assert data["cam"][0] == "https://smart-hub.io/cam1"
    assert data["cam"][1] == "https://smart-hub.io/cam2"
    assert data["stream"]["m4"] == "https://smart-hub.io/m4"
    assert data["stream"]["mjpeg"] == "https://smart-hub.io/mjpeg"
    assert data["stream"]["ustream"] == "https://smart-hub.io/ustream"
    assert data["feeds"]["blog"]["url"] == "https://smart-hub.io/blog"
    assert data["feeds"]["wiki"]["type"] == "mediawiki"
    assert data["feeds"]["wiki"]["url"] == "https://smart-hub.io/wiki"
    assert data["feeds"]["calendar"]["type"] == "ical"
    assert data["feeds"]["calendar"]["url"] == "https://smart-hub.io/calendar"
    assert (
        data["feeds"]["flicker"]["url"]
        == "https://www.flickr.com/photos/smart-hub"
    )
    assert data["cache"]["schedule"] == "m.02"
    assert data["projects"][0] == "https://smart-hub.io/projects/1"
    assert data["projects"][1] == "https://smart-hub.io/projects/2"
    assert data["projects"][2] == "https://smart-hub.io/projects/3"
    assert data["radio_show"][0]["name"] == "Radioshow"
    assert data["radio_show"][0]["url"] == "https://smart-hub.io/radio"
    assert data["radio_show"][0]["type"] == "ogg"
    assert data["radio_show"][0]["start"] == "2019-09-02T10:00Z"
    assert data["radio_show"][0]["end"] == "2019-09-02T12:00Z"


async def test_spaceapi_state_get(hass: SmartHub, mock_client) -> None:
    """Test response if the state entity was set."""
    hass.states.async_set("test.test_door", True)

    resp = await mock_client.get(URL_API_SPACEAPI)
    assert resp.status == HTTPStatus.OK

    data = await resp.json()
    assert data["state"]["open"] == bool(1)


async def test_spaceapi_sensors_get(hass: SmartHub, mock_client) -> None:
    """Test the response for the sensors."""
    resp = await mock_client.get(URL_API_SPACEAPI)
    assert resp.status == HTTPStatus.OK

    data = await resp.json()
    assert data["sensors"] == SENSOR_OUTPUT
