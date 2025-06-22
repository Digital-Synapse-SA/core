"""Test the setup of the Youless integration."""

from smarthub import setup
from smarthub.components import youless
from smarthub.config_entries import ConfigEntryState
from smarthub.core import SmartHub

from . import init_component


async def test_async_setup_entry(hass: SmartHub) -> None:
    """Check if the setup of the integration succeeds."""

    entry = await init_component(hass)

    assert await setup.async_setup_component(hass, youless.DOMAIN, {})
    assert entry.state is ConfigEntryState.LOADED
    assert len(hass.states.async_entity_ids()) == 22
