"""Exceptions for the dwd_weather_warnings integration."""

from smarthub.exceptions import SmartHubError


class EntityNotFoundError(SmartHubError):
    """When a referenced entity was not found."""
