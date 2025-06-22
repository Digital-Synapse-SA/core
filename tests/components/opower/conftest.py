"""Fixtures for the Opower integration tests."""

import pytest

from smarthub.components.opower.const import DOMAIN
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


@pytest.fixture
def mock_config_entry(hass: SmartHub) -> MockConfigEntry:
    """Return the default mocked config entry."""
    config_entry = MockConfigEntry(
        title="Pacific Gas & Electric (test-username)",
        domain=DOMAIN,
        data={
            "utility": "Pacific Gas and Electric Company (PG&E)",
            "username": "test-username",
            "password": "test-password",
        },
    )
    config_entry.add_to_hass(hass)
    return config_entry
