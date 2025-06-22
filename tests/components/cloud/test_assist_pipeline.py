"""Test the cloud assist pipeline."""

import pytest

from smarthub.components.cloud.assist_pipeline import (
    async_migrate_cloud_pipeline_engine,
)
from smarthub.const import Platform
from smarthub.core import SmartHub
from smarthub.setup import async_setup_component


async def test_migrate_pipeline_invalid_platform(hass: SmartHub) -> None:
    """Test migrate pipeline with invalid platform."""
    await async_setup_component(hass, "assist_pipeline", {})
    with pytest.raises(ValueError):
        await async_migrate_cloud_pipeline_engine(
            hass, Platform.BINARY_SENSOR, "test-engine-id"
        )
