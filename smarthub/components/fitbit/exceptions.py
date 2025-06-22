"""Exceptions for fitbit API calls.

These exceptions exist to provide common exceptions for the async and sync client libraries.
"""

from smarthub.exceptions import SmartHubError


class FitbitApiException(SmartHubError):
    """Error talking to the fitbit API."""


class FitbitAuthException(FitbitApiException):
    """Authentication related error talking to the fitbit API."""
