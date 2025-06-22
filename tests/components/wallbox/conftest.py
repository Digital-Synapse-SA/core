"""Test fixtures for the Wallbox integration."""

import pytest

from smarthub.components.wallbox.const import CONF_STATION, DOMAIN
from smarthub.const import CONF_PASSWORD, CONF_USERNAME
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


@pytest.fixture
def entry(hass: SmartHub) -> MockConfigEntry:
    """Return mock config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_USERNAME: "test_username",
            CONF_PASSWORD: "test_password",
            CONF_STATION: "12345",
        },
        entry_id="testEntry",
    )
    entry.add_to_hass(hass)
    return entry
