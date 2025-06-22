"""Shopping list test helpers."""

from unittest.mock import patch

import pytest

from smarthub.components.shopping_list import intent as sl_intent
from smarthub.core import SmartHub

from tests.common import MockConfigEntry


@pytest.fixture(autouse=True)
def mock_shopping_list_io():
    """Stub out the persistence."""
    with (
        patch("smarthub.components.shopping_list.ShoppingData.save"),
        patch("smarthub.components.shopping_list.ShoppingData.async_load"),
    ):
        yield


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Config Entry fixture."""
    return MockConfigEntry(domain="shopping_list")


@pytest.fixture
async def sl_setup(hass: SmartHub, mock_config_entry: MockConfigEntry):
    """Set up the shopping list."""

    mock_config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    await sl_intent.async_setup_intents(hass)
