"""Light conftest."""

from unittest.mock import AsyncMock, patch

import pytest

from smarthub.components.light import Profiles
from smarthub.core import SmartHub


@pytest.fixture(autouse=True)
def mock_light_profiles():
    """Mock loading of profiles."""
    data = {}

    def mock_profiles_class(hass: SmartHub) -> Profiles:
        profiles = Profiles(hass)
        profiles.data = data
        profiles.async_initialize = AsyncMock()
        return profiles

    with patch(
        "smarthub.components.light.Profiles",
        side_effect=mock_profiles_class,
    ):
        yield data
