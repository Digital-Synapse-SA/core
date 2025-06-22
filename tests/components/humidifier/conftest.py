"""Fixtures for Humidifier platform tests."""

from collections.abc import Generator

import pytest

from smarthub.config_entries import ConfigEntry, ConfigFlow
from smarthub.const import Platform
from smarthub.core import SmartHub

from tests.common import (
    MockConfigEntry,
    MockModule,
    mock_config_flow,
    mock_integration,
    mock_platform,
)


class MockFlow(ConfigFlow):
    """Test flow."""


@pytest.fixture
def config_flow_fixture(hass: SmartHub) -> Generator[None]:
    """Mock config flow."""
    mock_platform(hass, "test.config_flow")

    with mock_config_flow("test", MockFlow):
        yield


@pytest.fixture
def register_test_integration(
    hass: SmartHub, config_flow_fixture: None
) -> Generator:
    """Provide a mocked integration for tests."""

    config_entry = MockConfigEntry(domain="test")
    config_entry.add_to_hass(hass)

    async def help_async_setup_entry_init(
        hass: SmartHub, config_entry: ConfigEntry
    ) -> bool:
        """Set up test config entry."""
        await hass.config_entries.async_forward_entry_setups(
            config_entry, [Platform.HUMIDIFIER]
        )
        return True

    async def help_async_unload_entry(
        hass: SmartHub, config_entry: ConfigEntry
    ) -> bool:
        """Unload test config emntry."""
        return await hass.config_entries.async_unload_platforms(
            config_entry, [Platform.HUMIDIFIER]
        )

    mock_integration(
        hass,
        MockModule(
            "test",
            async_setup_entry=help_async_setup_entry_init,
            async_unload_entry=help_async_unload_entry,
        ),
    )

    return config_entry
