"""Tests for the devolo Home Network integration."""

from smarthub.components.devolo_home_network.const import DOMAIN
from smarthub.const import CONF_IP_ADDRESS, CONF_PASSWORD
from smarthub.core import SmartHub

from .const import DISCOVERY_INFO, IP

from tests.common import MockConfigEntry


def configure_integration(hass: SmartHub) -> MockConfigEntry:
    """Configure the integration."""
    config = {
        CONF_IP_ADDRESS: IP,
        CONF_PASSWORD: "test",
    }
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=config,
        entry_id="123456",
        unique_id=DISCOVERY_INFO.properties["SN"],
    )
    entry.add_to_hass(hass)

    return entry
