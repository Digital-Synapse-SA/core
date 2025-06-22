"""The test for the Melissa Climate component."""

from smarthub.core import SmartHub

from . import setup_integration


async def test_setup(hass: SmartHub, mock_melissa) -> None:
    """Test setting up the Melissa component."""
    await setup_integration(hass)

    mock_melissa.assert_called_with(username="********", password="********")
