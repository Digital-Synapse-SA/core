"""Tests Ollama integration."""

from typing import Any
from unittest.mock import patch

import pytest

from smarthub.components import ollama
from smarthub.const import CONF_LLM_HASS_API
from smarthub.core import SmartHub
from smarthub.helpers import llm
from smarthub.setup import async_setup_component

from . import TEST_OPTIONS, TEST_USER_DATA

from tests.common import MockConfigEntry


@pytest.fixture
def mock_config_entry_options() -> dict[str, Any]:
    """Fixture for configuration entry options."""
    return TEST_OPTIONS


@pytest.fixture
def mock_config_entry(
    hass: SmartHub, mock_config_entry_options: dict[str, Any]
) -> MockConfigEntry:
    """Mock a config entry."""
    entry = MockConfigEntry(
        domain=ollama.DOMAIN,
        data=TEST_USER_DATA,
        options=mock_config_entry_options,
    )
    entry.add_to_hass(hass)
    return entry


@pytest.fixture
def mock_config_entry_with_assist(
    hass: SmartHub, mock_config_entry: MockConfigEntry
) -> MockConfigEntry:
    """Mock a config entry with assist."""
    hass.config_entries.async_update_entry(
        mock_config_entry, options={CONF_LLM_HASS_API: llm.LLM_API_ASSIST}
    )
    return mock_config_entry


@pytest.fixture
async def mock_init_component(hass: SmartHub, mock_config_entry: MockConfigEntry):
    """Initialize integration."""
    assert await async_setup_component(hass, "smarthub", {})

    with patch(
        "ollama.AsyncClient.list",
    ):
        assert await async_setup_component(hass, ollama.DOMAIN, {})
        await hass.async_block_till_done()
        yield


@pytest.fixture(autouse=True)
async def setup_ha(hass: SmartHub) -> None:
    """Set up SmartHub."""
    assert await async_setup_component(hass, "smarthub", {})
