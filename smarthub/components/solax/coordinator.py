"""Constants for the solax integration."""

from solax import InverterResponse

from smarthub.helpers.update_coordinator import DataUpdateCoordinator


class SolaxDataUpdateCoordinator(DataUpdateCoordinator[InverterResponse]):
    """DataUpdateCoordinator for solax."""
