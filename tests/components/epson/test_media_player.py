"""Tests for the epson integration."""

from datetime import timedelta
from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory

from smarthub.components.epson.const import CONF_CONNECTION_TYPE, DOMAIN, HTTP
from smarthub.const import CONF_HOST
from smarthub.core import SmartHub
from smarthub.helpers import entity_registry as er

from tests.common import MockConfigEntry, async_fire_time_changed


async def test_set_unique_id(
    hass: SmartHub,
    entity_registry: er.EntityRegistry,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test the unique id is set on runtime."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Epson",
        data={CONF_CONNECTION_TYPE: HTTP, CONF_HOST: "1.1.1.1"},
        entry_id="1cb78c095906279574a0442a1f0003ef",
    )
    entry.add_to_hass(hass)
    with patch("smarthub.components.epson.Projector.get_power"):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        assert entry.unique_id is None
        entity_entry = entity_registry.async_get("media_player.epson")
        assert entity_entry
        assert entity_entry.unique_id == entry.entry_id
    with (
        patch("smarthub.components.epson.Projector.get_power", return_value="01"),
        patch(
            "smarthub.components.epson.Projector.get_serial_number",
            return_value="123",
        ),
        patch(
            "smarthub.components.epson.Projector.get_property",
        ),
    ):
        freezer.tick(timedelta(seconds=30))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()
        entity_entry = entity_registry.async_get("media_player.epson")
        assert entity_entry
        assert entity_entry.unique_id == "123"
        assert entry.unique_id == "123"
