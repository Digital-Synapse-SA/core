"""Test the Fjäråskupan coordinator module."""

from fjaraskupan import (
    FjaraskupanConnectionError,
    FjaraskupanError,
    FjaraskupanReadError,
    FjaraskupanWriteError,
)
import pytest

from smarthub.components.fjaraskupan.const import DOMAIN
from smarthub.components.fjaraskupan.coordinator import exception_converter
from smarthub.exceptions import SmartHubError


@pytest.mark.parametrize(
    ("exception", "translation_key", "translation_placeholder"),
    [
        (FjaraskupanReadError(), "read_error", None),
        (FjaraskupanWriteError(), "write_error", None),
        (FjaraskupanConnectionError(), "connection_error", None),
        (FjaraskupanError("Some error"), "unexpected_error", {"msg": "Some error"}),
    ],
)
def test_exeception_wrapper(
    exception: Exception, translation_key: str, translation_placeholder: dict[str, str]
) -> None:
    """Test our exception conversion."""
    with pytest.raises(SmartHubError) as exc_info, exception_converter():
        raise exception
    assert exc_info.value.translation_domain == DOMAIN
    assert exc_info.value.translation_key == translation_key
    assert exc_info.value.translation_placeholders == translation_placeholder
