"""Device automation exceptions."""

from smarthub.exceptions import SmartHubError


class InvalidDeviceAutomationConfig(SmartHubError):
    """When device automation config is invalid."""


class DeviceNotFound(SmartHubError):
    """When referenced device not found."""


class EntityNotFound(SmartHubError):
    """When referenced entity not found."""
