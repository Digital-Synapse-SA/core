"""The tests for the geolocation component."""

import pytest

from smarthub.components import geo_location
from smarthub.components.geo_location import GeolocationEvent
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component


async def test_setup_component(hass: SmartHub) -> None:
    """Simple test setup of component."""
    result = await async_setup_component(hass, geo_location.DOMAIN, {})
    assert result


async def test_event(hass: SmartHub) -> None:
    """Simple test of the geolocation event class."""
    entity = GeolocationEvent()

    assert entity.state is None
    assert entity.distance is None
    assert entity.latitude is None
    assert entity.longitude is None
    with pytest.raises(AttributeError):
        assert entity.source is None
