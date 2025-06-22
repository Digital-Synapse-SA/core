"""WebSocket API related errors."""

from smarthub.exceptions import SmartHubError


class Disconnect(SmartHubError):
    """Disconnect the current session."""
