"""Tests for the Plaato integration."""

from unittest.mock import patch

from freezegun import freeze_time
from pyplaato.models.airlock import PlaatoAirlock
from pyplaato.models.device import PlaatoDeviceType
from pyplaato.models.keg import PlaatoKeg

from smarthub.components.plaato.const import (
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_USE_WEBHOOK,
    DOMAIN,
)
from smarthub.const import CONF_TOKEN
from smarthub.core import SmartHub

from tests.common import MockConfigEntry

# Note: It would be good to replace this test data
# with actual data from the API
AIRLOCK_DATA = {}
KEG_DATA = {}


@freeze_time("2024-05-24 12:00:00", tz_offset=0)
async def init_integration(
    hass: SmartHub, device_type: PlaatoDeviceType
) -> MockConfigEntry:
    """Mock integration setup."""
    with (
        patch(
            "smarthub.components.plaato.coordinator.Plaato.get_airlock_data",
            return_value=PlaatoAirlock(AIRLOCK_DATA),
        ),
        patch(
            "smarthub.components.plaato.coordinator.Plaato.get_keg_data",
            return_value=PlaatoKeg(KEG_DATA),
        ),
    ):
        entry = MockConfigEntry(
            domain=DOMAIN,
            data={
                CONF_USE_WEBHOOK: False,
                CONF_TOKEN: "valid_token",
                CONF_DEVICE_TYPE: device_type,
                CONF_DEVICE_NAME: "device_name",
            },
            entry_id="123456",
        )
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    return entry
