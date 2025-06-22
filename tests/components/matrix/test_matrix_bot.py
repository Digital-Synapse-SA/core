"""Configure and test MatrixBot."""

from smarthub.components.matrix import MatrixBot
from smarthub.components.matrix.const import DOMAIN, SERVICE_SEND_MESSAGE
from smarthub.components.notify import DOMAIN as NOTIFY_DOMAIN
from smarthub.core import SmartHub

from .conftest import TEST_NOTIFIER_NAME


async def test_services(hass: SmartHub, matrix_bot: MatrixBot) -> None:
    """Test hass/MatrixBot state."""

    services = hass.services.async_services()

    # Verify that the matrix service is registered
    assert (matrix_service := services.get(DOMAIN))
    assert SERVICE_SEND_MESSAGE in matrix_service

    # Verify that the matrix notifier is registered
    assert (notify_service := services.get(NOTIFY_DOMAIN))
    assert TEST_NOTIFIER_NAME in notify_service
