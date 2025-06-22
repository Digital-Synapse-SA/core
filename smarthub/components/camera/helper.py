"""Camera helper functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from smarthub.core import SmartHub
from smarthub.exceptions import SmartHubError

from .const import DATA_COMPONENT

if TYPE_CHECKING:
    from . import Camera


def get_camera_from_entity_id(hass: SmartHub, entity_id: str) -> Camera:
    """Get camera component from entity_id."""
    component = hass.data.get(DATA_COMPONENT)
    if component is None:
        raise SmartHubError("Camera integration not set up")

    if (camera := component.get_entity(entity_id)) is None:
        raise SmartHubError("Camera not found")

    if not camera.is_on:
        raise SmartHubError("Camera is off")

    return camera
