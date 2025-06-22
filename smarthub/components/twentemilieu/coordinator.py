"""Data update coordinator for Twente Milieu."""

from __future__ import annotations

from datetime import date

from twentemilieu import TwenteMilieu, WasteType

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.helpers.aiohttp_client import async_get_clientsession
from smarthub.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_HOUSE_LETTER,
    CONF_HOUSE_NUMBER,
    CONF_POST_CODE,
    DOMAIN,
    LOGGER,
    SCAN_INTERVAL,
)

type TwenteMilieuConfigEntry = ConfigEntry[TwenteMilieuDataUpdateCoordinator]


class TwenteMilieuDataUpdateCoordinator(
    DataUpdateCoordinator[dict[WasteType, list[date]]]
):
    """Class to manage fetching Twente Milieu data."""

    def __init__(self, hass: SmartHub, entry: TwenteMilieuConfigEntry) -> None:
        """Initialize Twente Milieu data update coordinator."""
        self.twentemilieu = TwenteMilieu(
            post_code=entry.data[CONF_POST_CODE],
            house_number=entry.data[CONF_HOUSE_NUMBER],
            house_letter=entry.data[CONF_HOUSE_LETTER],
            session=async_get_clientsession(hass),
        )
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
            config_entry=entry,
        )

    async def _async_update_data(self) -> dict[WasteType, list[date]]:
        """Fetch Twente Milieu data."""
        return await self.twentemilieu.update()
