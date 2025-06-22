"""Errors for the Konnected component."""

from smarthub.exceptions import SmartHubError


class KonnectedException(SmartHubError):
    """Base class for Konnected exceptions."""


class CannotConnect(KonnectedException):
    """Unable to connect to the panel."""
