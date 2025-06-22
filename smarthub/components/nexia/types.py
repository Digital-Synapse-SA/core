"""Support for Nexia / Trane XL Thermostats."""

from smarthub.config_entries import ConfigEntry

from .coordinator import NexiaDataUpdateCoordinator

type NexiaConfigEntry = ConfigEntry[NexiaDataUpdateCoordinator]
