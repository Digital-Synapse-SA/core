"""Test init."""

from unittest.mock import patch

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub


async def test_cannot_connect(
    hass: SmartHub, stt_config_entry: ConfigEntry
) -> None:
    """Test we handle cannot connect error."""
    with patch(
        "smarthub.components.wyoming.data.load_wyoming_info",
        return_value=None,
    ):
        assert not await hass.config_entries.async_setup(stt_config_entry.entry_id)


async def test_unload(
    hass: SmartHub, stt_config_entry: ConfigEntry, init_wyoming_stt
) -> None:
    """Test unload."""
    assert await hass.config_entries.async_unload(stt_config_entry.entry_id)
