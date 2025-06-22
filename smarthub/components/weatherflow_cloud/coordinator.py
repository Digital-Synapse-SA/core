"""Data coordinator for WeatherFlow Cloud Data."""

from datetime import timedelta

from aiohttp import ClientResponseError
from weatherflow4py.api import WeatherFlowRestAPI
from weatherflow4py.models.rest.unified import WeatherFlowDataREST

from smarthub.config_entries import ConfigEntry
from smarthub.const import CONF_API_TOKEN
from smarthub.core import SmartHub
from smarthub.exceptions import ConfigEntryAuthFailed
from smarthub.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER


class WeatherFlowCloudDataUpdateCoordinator(
    DataUpdateCoordinator[dict[int, WeatherFlowDataREST]]
):
    """Class to manage fetching REST Based WeatherFlow Forecast data."""

    config_entry: ConfigEntry

    def __init__(self, hass: SmartHub, config_entry: ConfigEntry) -> None:
        """Initialize global WeatherFlow forecast data updater."""
        self.weather_api = WeatherFlowRestAPI(
            api_token=config_entry.data[CONF_API_TOKEN]
        )
        super().__init__(
            hass,
            LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self) -> dict[int, WeatherFlowDataREST]:
        """Fetch data from WeatherFlow Forecast."""
        try:
            async with self.weather_api:
                return await self.weather_api.get_all_data()
        except ClientResponseError as err:
            if err.status == 401:
                raise ConfigEntryAuthFailed(err) from err
            raise UpdateFailed(f"Update failed: {err}") from err
