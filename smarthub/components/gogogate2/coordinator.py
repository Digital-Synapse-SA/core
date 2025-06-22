"""Coordinator for GogoGate2 component."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from datetime import timedelta
import logging

from ismartgate import AbstractGateApi, GogoGate2InfoResponse, ISmartGateInfoResponse

from smarthub.config_entries import ConfigEntry
from smarthub.core import SmartHub
from smarthub.helpers.debounce import Debouncer
from smarthub.helpers.update_coordinator import DataUpdateCoordinator

type GogoGateConfigEntry = ConfigEntry[DeviceDataUpdateCoordinator]


class DeviceDataUpdateCoordinator(
    DataUpdateCoordinator[GogoGate2InfoResponse | ISmartGateInfoResponse]
):
    """Manages polling for state changes from the device."""

    config_entry: GogoGateConfigEntry

    def __init__(
        self,
        hass: SmartHub,
        config_entry: GogoGateConfigEntry,
        logger: logging.Logger,
        api: AbstractGateApi,
        *,
        name: str,
        update_interval: timedelta,
        update_method: Callable[
            [], Awaitable[GogoGate2InfoResponse | ISmartGateInfoResponse]
        ]
        | None = None,
        request_refresh_debouncer: Debouncer | None = None,
    ) -> None:
        """Initialize the data update coordinator."""
        super().__init__(
            hass,
            logger,
            config_entry=config_entry,
            name=name,
            update_interval=update_interval,
            update_method=update_method,
            request_refresh_debouncer=request_refresh_debouncer,
        )
        self.api = api
