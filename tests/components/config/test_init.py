"""Test config init."""

from smarthub.core import SmartHub
from smarthub.setup import async_setup_component


async def test_config_setup(hass: SmartHub) -> None:
    """Test it sets up hassbian."""
    await async_setup_component(hass, "config", {})
    assert "config" in hass.config.components
