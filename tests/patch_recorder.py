"""Patch recorder related functions."""

from __future__ import annotations

from contextlib import contextmanager
import sys

# Patch recorder util session scope
from smarthub.helpers import recorder as recorder_helper

# Make sure smarthub.components.recorder.util is not already imported
assert "smarthub.components.recorder.util" not in sys.modules

real_session_scope = recorder_helper.session_scope


@contextmanager
def _session_scope_wrapper(*args, **kwargs):
    """Make session_scope patchable.

    This function will be imported by recorder modules.
    """
    with real_session_scope(*args, **kwargs) as ses:
        yield ses


recorder_helper.session_scope = _session_scope_wrapper
