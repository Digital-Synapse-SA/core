"""Test the my init."""

from unittest import mock

from smarthub.components.my import URL_PATH
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component


async def test_setup(hass: SmartHub) -> None:
    """Test setup."""
    with mock.patch(
        "smarthub.components.frontend.async_register_built_in_panel"
    ) as mock_register_panel:
        assert await async_setup_component(hass, "my", {"foo": "bar"})
        assert mock_register_panel.call_args == mock.call(
            hass, "my", frontend_url_path=URL_PATH
        )
