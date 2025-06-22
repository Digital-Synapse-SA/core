"""Helper to test significant Camera state changes."""

from __future__ import annotations

from typing import Any

from smarthub.core import SmartHub, callback


@callback
def async_check_significant_change(
    hass: SmartHub,
    old_state: str,
    old_attrs: dict,
    new_state: str,
    new_attrs: dict,
    **kwargs: Any,
) -> bool | None:
    """Test if state significantly changed."""
    if old_state != new_state:
        return True

    return None
