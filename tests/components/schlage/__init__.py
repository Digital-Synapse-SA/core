"""Tests for the Schlage integration."""

from smarthub.components.schlage.coordinator import SchlageDataUpdateCoordinator

from tests.common import MockConfigEntry

type MockSchlageConfigEntry = MockConfigEntry[SchlageDataUpdateCoordinator]
