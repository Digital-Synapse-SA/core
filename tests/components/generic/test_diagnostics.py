"""Test generic (IP camera) diagnostics."""

import pytest

from smarthub.components.diagnostics import REDACTED
from smarthub.components.generic.diagnostics import redact_url
from smarthub.core import SmartHub

from tests.common import MockConfigEntry
from tests.components.diagnostics import get_diagnostics_for_config_entry
from tests.typing import ClientSessionGenerator


async def test_entry_diagnostics(
    hass: SmartHub,
    hass_client: ClientSessionGenerator,
    setup_entry: MockConfigEntry,
) -> None:
    """Test config entry diagnostics."""

    assert await get_diagnostics_for_config_entry(hass, hass_client, setup_entry) == {
        "title": "Test Camera",
        "data": {},
        "options": {
            "still_image_url": "http://****:****@example.com/****?****=****",
            "stream_source": "http://****:****@example.com/****",
            "username": REDACTED,
            "password": REDACTED,
            "limit_refetch_to_url_change": False,
            "authentication": "basic",
            "framerate": 2.0,
            "verify_ssl": True,
            "content_type": "image/jpeg",
        },
    }


@pytest.mark.parametrize(
    ("url_in", "url_out_expected"),
    [
        (
            "http://www.example.com",
            "http://www.example.com",
        ),
        (
            "http://fred:letmein1@www.example.com/image.php?key=secret2",
            "http://****:****@www.example.com/****?****=****",
        ),
        (
            "http://fred@www.example.com/image.php?key=secret2",
            "http://****@www.example.com/****?****=****",
        ),
        (
            "http://fred@www.example.com/image.php",
            "http://****@www.example.com/****",
        ),
        (
            "http://:letmein1@www.example.com",
            "http://:****@www.example.com",
        ),
    ],
)
def test_redact_url(url_in, url_out_expected) -> None:
    """Test url redaction."""
    url_out = redact_url(url_in)
    assert url_out == url_out_expected
