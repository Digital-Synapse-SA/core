"""Exceptions for Google Tasks api calls."""

from smarthub.exceptions import SmartHubError


class GoogleTasksApiError(SmartHubError):
    """Error talking to the Google Tasks API."""
