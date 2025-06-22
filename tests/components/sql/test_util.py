"""Test the sql utils."""

from smarthub.components.recorder import Recorder, get_instance
from smarthub.components.sql.util import resolve_db_url
from smarthub.core import SmartHub


async def test_resolve_db_url_when_none_configured(
    recorder_mock: Recorder,
    hass: SmartHub,
) -> None:
    """Test return recorder db_url if provided db_url is None."""
    db_url = None
    resolved_url = resolve_db_url(hass, db_url)

    assert resolved_url == get_instance(hass).db_url


async def test_resolve_db_url_when_configured(hass: SmartHub) -> None:
    """Test return provided db_url if it's set."""
    db_url = "mssql://"
    resolved_url = resolve_db_url(hass, db_url)

    assert resolved_url == db_url
