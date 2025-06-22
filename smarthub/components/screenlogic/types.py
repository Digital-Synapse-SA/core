"""The Screenlogic integration."""

from smarthub.config_entries import ConfigEntry

from .coordinator import ScreenlogicDataUpdateCoordinator

type ScreenLogicConfigEntry = ConfigEntry[ScreenlogicDataUpdateCoordinator]
