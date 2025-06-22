"""Exceptions specific to volvooncall."""

from smarthub.exceptions import SmartHubError


class InvalidAuth(SmartHubError):
    """Error to indicate there is invalid auth."""
