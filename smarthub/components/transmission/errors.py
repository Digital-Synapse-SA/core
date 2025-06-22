"""Errors for the Transmission component."""

from smarthub.exceptions import SmartHubError


class AuthenticationError(SmartHubError):
    """Wrong Username or Password."""


class CannotConnect(SmartHubError):
    """Unable to connect to client."""


class UnknownError(SmartHubError):
    """Unknown Error."""
