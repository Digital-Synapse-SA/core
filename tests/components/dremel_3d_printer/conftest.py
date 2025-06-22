"""Configure tests for the Dremel 3D Printer integration."""

from http import HTTPStatus
from unittest.mock import patch

import pytest
import requests_mock

from smarthub.components.dremel_3d_printer.const import DOMAIN
from smarthub.const import CONF_HOST
from smarthub.core import SmartHub

from tests.common import MockConfigEntry, load_fixture

HOST = "1.2.3.4"
CONF_DATA = {CONF_HOST: HOST}


def create_entry(hass: SmartHub) -> MockConfigEntry:
    """Create fixture for adding config entry in SmartHub."""
    entry = MockConfigEntry(domain=DOMAIN, data=CONF_DATA, unique_id="123456789")
    entry.add_to_hass(hass)
    return entry


@pytest.fixture
def config_entry(hass: SmartHub) -> MockConfigEntry:
    """Add config entry in SmartHub."""
    return create_entry(hass)


@pytest.fixture
def connection() -> None:
    """Mock Dremel 3D Printer connection."""
    with requests_mock.Mocker() as mock:
        mock.post(
            f"http://{HOST}/command",
            response_list=[
                {"text": load_fixture("dremel_3d_printer/command_1.json")},
                {"text": load_fixture("dremel_3d_printer/command_2.json")},
                {"text": load_fixture("dremel_3d_printer/command_1.json")},
                {"text": load_fixture("dremel_3d_printer/command_2.json")},
            ],
        )

        mock.post(
            f"https://{HOST}:11134/getHomeMessage",
            text=load_fixture("dremel_3d_printer/get_home_message.json"),
            status_code=HTTPStatus.OK,
        )
        yield


def patch_async_setup_entry():
    """Patch the async entry setup of Dremel 3D Printer."""
    return patch(
        "smarthub.components.dremel_3d_printer.async_setup_entry",
        return_value=True,
    )
