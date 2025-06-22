"""Types for the Model Context Protocol integration."""

from smarthub.config_entries import ConfigEntry

from .coordinator import ModelContextProtocolCoordinator

type ModelContextProtocolConfigEntry = ConfigEntry[ModelContextProtocolCoordinator]
