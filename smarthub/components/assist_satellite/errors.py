"""Errors for assist satellite."""

from smarthub.exceptions import SmartHubError


class AssistSatelliteError(SmartHubError):
    """Base class for assist satellite errors."""


class SatelliteBusyError(AssistSatelliteError):
    """Satellite is busy and cannot handle the request."""
