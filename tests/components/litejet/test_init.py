"""The tests for the litejet component."""

from smarthub.components import litejet
from smarthub.components.litejet.const import DOMAIN
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component

from . import async_init_integration


async def test_setup_with_no_config(hass: SmartHub) -> None:
    """Test that nothing happens."""
    assert await async_setup_component(hass, DOMAIN, {}) is True
    assert DOMAIN not in hass.data


async def test_unload_entry(hass: SmartHub, mock_litejet) -> None:
    """Test being able to unload an entry."""
    entry = await async_init_integration(hass, use_switch=True, use_scene=True)

    assert await litejet.async_unload_entry(hass, entry)
    assert DOMAIN not in hass.data
