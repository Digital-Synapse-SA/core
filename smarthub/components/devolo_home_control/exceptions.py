"""Custom exceptions for the devolo_home_control integration."""

from smarthub.exceptions import SmartHubError


class CredentialsInvalid(SmartHubError):
    """Given credentials are invalid."""


class UuidChanged(SmartHubError):
    """UUID of the user changed."""
