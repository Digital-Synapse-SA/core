"""Test the aiohttp client helper."""

import socket
from unittest.mock import Mock, patch

import aiohttp
from aiohttp.test_utils import TestClient
import pytest

from smarthub.components.mjpeg import (
    CONF_MJPEG_URL,
    CONF_STILL_IMAGE_URL,
    DOMAIN as MJPEG_DOMAIN,
)
from smarthub.const import (
    CONF_AUTHENTICATION,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_VERIFY_SSL,
    EVENT_HOMEASSISTANT_CLOSE,
    HTTP_BASIC_AUTHENTICATION,
)
from smarthub.core import SmartHub
from smarthub.helpers import aiohttp_client as client
from smarthub.util.color import RGBColor
from smarthub.util.ssl import SSLCipherList

from tests.common import (
    MockConfigEntry,
    MockModule,
    extract_stack_to_frame,
    mock_integration,
)
from tests.test_util.aiohttp import AiohttpClientMocker
from tests.typing import ClientSessionGenerator


@pytest.fixture(name="camera_client")
async def camera_client_fixture(
    hass: SmartHub, hass_client: ClientSessionGenerator
) -> TestClient:
    """Fixture to fetch camera streams."""
    mock_config_entry = MockConfigEntry(
        title="MJPEG Camera",
        domain=MJPEG_DOMAIN,
        options={
            CONF_AUTHENTICATION: HTTP_BASIC_AUTHENTICATION,
            CONF_MJPEG_URL: "http://example.com/mjpeg_stream",
            CONF_PASSWORD: None,
            CONF_STILL_IMAGE_URL: None,
            CONF_USERNAME: None,
            CONF_VERIFY_SSL: True,
        },
    )
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    return await hass_client()


async def test_get_clientsession_with_ssl(hass: SmartHub) -> None:
    """Test init clientsession with ssl."""
    client.async_get_clientsession(hass)
    verify_ssl = True
    ssl_cipher = SSLCipherList.PYTHON_DEFAULT
    family = 0

    client_session = hass.data[client.DATA_CLIENTSESSION][
        (verify_ssl, family, ssl_cipher)
    ]
    assert isinstance(client_session, aiohttp.ClientSession)
    connector = hass.data[client.DATA_CONNECTOR][(verify_ssl, family, ssl_cipher)]
    assert isinstance(connector, aiohttp.TCPConnector)


async def test_get_clientsession_without_ssl(hass: SmartHub) -> None:
    """Test init clientsession without ssl."""
    client.async_get_clientsession(hass, verify_ssl=False)
    verify_ssl = False
    ssl_cipher = SSLCipherList.PYTHON_DEFAULT
    family = 0

    client_session = hass.data[client.DATA_CLIENTSESSION][
        (verify_ssl, family, ssl_cipher)
    ]
    assert isinstance(client_session, aiohttp.ClientSession)
    connector = hass.data[client.DATA_CONNECTOR][(verify_ssl, family, ssl_cipher)]
    assert isinstance(connector, aiohttp.TCPConnector)


@pytest.mark.parametrize(
    ("verify_ssl", "expected_family", "ssl_cipher"),
    [
        (True, socket.AF_UNSPEC, SSLCipherList.PYTHON_DEFAULT),
        (True, socket.AF_INET, SSLCipherList.PYTHON_DEFAULT),
        (True, socket.AF_INET6, SSLCipherList.PYTHON_DEFAULT),
        (True, socket.AF_UNSPEC, SSLCipherList.INTERMEDIATE),
        (True, socket.AF_INET, SSLCipherList.INTERMEDIATE),
        (True, socket.AF_INET6, SSLCipherList.INTERMEDIATE),
        (True, socket.AF_UNSPEC, SSLCipherList.MODERN),
        (True, socket.AF_INET, SSLCipherList.MODERN),
        (True, socket.AF_INET6, SSLCipherList.MODERN),
        (True, socket.AF_UNSPEC, SSLCipherList.INSECURE),
        (True, socket.AF_INET, SSLCipherList.INSECURE),
        (True, socket.AF_INET6, SSLCipherList.INSECURE),
        (False, socket.AF_UNSPEC, SSLCipherList.PYTHON_DEFAULT),
        (False, socket.AF_INET, SSLCipherList.PYTHON_DEFAULT),
        (False, socket.AF_INET6, SSLCipherList.PYTHON_DEFAULT),
        (False, socket.AF_UNSPEC, SSLCipherList.INTERMEDIATE),
        (False, socket.AF_INET, SSLCipherList.INTERMEDIATE),
        (False, socket.AF_INET6, SSLCipherList.INTERMEDIATE),
        (False, socket.AF_UNSPEC, SSLCipherList.MODERN),
        (False, socket.AF_INET, SSLCipherList.MODERN),
        (False, socket.AF_INET6, SSLCipherList.MODERN),
        (False, socket.AF_UNSPEC, SSLCipherList.INSECURE),
        (False, socket.AF_INET, SSLCipherList.INSECURE),
        (False, socket.AF_INET6, SSLCipherList.INSECURE),
    ],
)
async def test_get_clientsession(
    hass: SmartHub,
    verify_ssl: bool,
    expected_family: int,
    ssl_cipher: SSLCipherList,
) -> None:
    """Test init clientsession combinations."""
    client.async_get_clientsession(
        hass, verify_ssl=verify_ssl, family=expected_family, ssl_cipher=ssl_cipher
    )
    client_session = hass.data[client.DATA_CLIENTSESSION][
        (verify_ssl, expected_family, ssl_cipher)
    ]
    assert isinstance(client_session, aiohttp.ClientSession)
    connector = hass.data[client.DATA_CONNECTOR][
        (verify_ssl, expected_family, ssl_cipher)
    ]
    assert isinstance(connector, aiohttp.TCPConnector)


async def test_create_clientsession_with_ssl_and_cookies(hass: SmartHub) -> None:
    """Test create clientsession with ssl."""
    session = client.async_create_clientsession(hass, cookies={"bla": True})
    assert isinstance(session, aiohttp.ClientSession)

    verify_ssl = True
    ssl_cipher = SSLCipherList.PYTHON_DEFAULT
    family = 0

    assert client.DATA_CLIENTSESSION not in hass.data
    connector = hass.data[client.DATA_CONNECTOR][(verify_ssl, family, ssl_cipher)]
    assert isinstance(connector, aiohttp.TCPConnector)


async def test_create_clientsession_without_ssl_and_cookies(
    hass: SmartHub,
) -> None:
    """Test create clientsession without ssl."""
    session = client.async_create_clientsession(hass, False, cookies={"bla": True})
    assert isinstance(session, aiohttp.ClientSession)

    verify_ssl = False
    ssl_cipher = SSLCipherList.PYTHON_DEFAULT
    family = 0

    assert client.DATA_CLIENTSESSION not in hass.data
    connector = hass.data[client.DATA_CONNECTOR][(verify_ssl, family, ssl_cipher)]
    assert isinstance(connector, aiohttp.TCPConnector)


@pytest.mark.parametrize(
    ("verify_ssl", "expected_family", "ssl_cipher"),
    [
        (True, 0, SSLCipherList.PYTHON_DEFAULT),
        (True, 4, SSLCipherList.PYTHON_DEFAULT),
        (True, 6, SSLCipherList.PYTHON_DEFAULT),
        (True, 0, SSLCipherList.INTERMEDIATE),
        (True, 4, SSLCipherList.INTERMEDIATE),
        (True, 6, SSLCipherList.INTERMEDIATE),
        (True, 0, SSLCipherList.MODERN),
        (True, 4, SSLCipherList.MODERN),
        (True, 6, SSLCipherList.MODERN),
        (True, 0, SSLCipherList.INSECURE),
        (True, 4, SSLCipherList.INSECURE),
        (True, 6, SSLCipherList.INSECURE),
        (False, 0, SSLCipherList.PYTHON_DEFAULT),
        (False, 4, SSLCipherList.PYTHON_DEFAULT),
        (False, 6, SSLCipherList.PYTHON_DEFAULT),
        (False, 0, SSLCipherList.INTERMEDIATE),
        (False, 4, SSLCipherList.INTERMEDIATE),
        (False, 6, SSLCipherList.INTERMEDIATE),
        (False, 0, SSLCipherList.MODERN),
        (False, 4, SSLCipherList.MODERN),
        (False, 6, SSLCipherList.MODERN),
        (False, 0, SSLCipherList.INSECURE),
        (False, 4, SSLCipherList.INSECURE),
        (False, 6, SSLCipherList.INSECURE),
    ],
)
async def test_get_clientsession_cleanup(
    hass: SmartHub,
    verify_ssl: bool,
    expected_family: int,
    ssl_cipher: SSLCipherList,
) -> None:
    """Test init clientsession cleanup."""
    client.async_get_clientsession(
        hass, verify_ssl=verify_ssl, family=expected_family, ssl_cipher=ssl_cipher
    )

    client_session = hass.data[client.DATA_CLIENTSESSION][
        (verify_ssl, expected_family, ssl_cipher)
    ]
    assert isinstance(client_session, aiohttp.ClientSession)
    connector = hass.data[client.DATA_CONNECTOR][
        (verify_ssl, expected_family, ssl_cipher)
    ]
    assert isinstance(connector, aiohttp.TCPConnector)

    hass.bus.async_fire(EVENT_HOMEASSISTANT_CLOSE)
    await hass.async_block_till_done()

    assert client_session.closed
    assert connector.closed


async def test_get_clientsession_patched_close(hass: SmartHub) -> None:
    """Test closing clientsession does not work."""

    verify_ssl = True
    ssl_cipher = SSLCipherList.PYTHON_DEFAULT
    family = 0

    with patch("aiohttp.ClientSession.close") as mock_close:
        session = client.async_get_clientsession(hass)

        assert isinstance(
            hass.data[client.DATA_CLIENTSESSION][(verify_ssl, family, ssl_cipher)],
            aiohttp.ClientSession,
        )
        assert isinstance(
            hass.data[client.DATA_CONNECTOR][(verify_ssl, family, ssl_cipher)],
            aiohttp.TCPConnector,
        )

        with pytest.raises(RuntimeError):
            await session.close()

        assert mock_close.call_count == 0


async def test_warning_close_session_integration(
    hass: SmartHub, caplog: pytest.LogCaptureFixture
) -> None:
    """Test log warning message when closing the session from integration context."""
    with (
        patch(
            "smarthub.helpers.frame.linecache.getline",
            return_value="await session.close()",
        ),
        patch(
            "smarthub.helpers.frame.get_current_frame",
            return_value=extract_stack_to_frame(
                [
                    Mock(
                        filename="/home/paulus/smarthub/core.py",
                        lineno="23",
                        line="do_something()",
                    ),
                    Mock(
                        filename="/home/paulus/smarthub/components/hue/light.py",
                        lineno="23",
                        line="await session.close()",
                    ),
                    Mock(
                        filename="/home/paulus/aiohue/lights.py",
                        lineno="2",
                        line="something()",
                    ),
                ]
            ),
        ),
    ):
        session = client.async_get_clientsession(hass)
        await session.close()
    assert (
        "Detected that integration 'hue' closes the SmartHub aiohttp session at "
        "smarthub/components/hue/light.py, line 23: await session.close(). "
        "Please create a bug report at https://github.com/smart-hub/core/issues?"
        "q=is%3Aopen+is%3Aissue+label%3A%22integration%3A+hue%22"
    ) in caplog.text


async def test_warning_close_session_custom(
    hass: SmartHub, caplog: pytest.LogCaptureFixture
) -> None:
    """Test log warning message when closing the session from custom context."""
    mock_integration(hass, MockModule("hue"), built_in=False)
    with (
        patch(
            "smarthub.helpers.frame.linecache.getline",
            return_value="await session.close()",
        ),
        patch(
            "smarthub.helpers.frame.get_current_frame",
            return_value=extract_stack_to_frame(
                [
                    Mock(
                        filename="/home/paulus/smarthub/core.py",
                        lineno="23",
                        line="do_something()",
                    ),
                    Mock(
                        filename="/home/paulus/config/custom_components/hue/light.py",
                        lineno="23",
                        line="await session.close()",
                    ),
                    Mock(
                        filename="/home/paulus/aiohue/lights.py",
                        lineno="2",
                        line="something()",
                    ),
                ]
            ),
        ),
    ):
        session = client.async_get_clientsession(hass)
        await session.close()
    assert (
        "Detected that custom integration 'hue' closes the SmartHub aiohttp "
        "session at custom_components/hue/light.py, line 23: await session.close(). "
        "Please report it to the author of the 'hue' custom integration"
    ) in caplog.text


async def test_async_aiohttp_proxy_stream(
    aioclient_mock: AiohttpClientMocker, camera_client: TestClient
) -> None:
    """Test that it fetches the given url."""
    aioclient_mock.get("http://example.com/mjpeg_stream", content=b"Frame1Frame2Frame3")

    resp = await camera_client.get("/api/camera_proxy_stream/camera.mjpeg_camera")

    assert resp.status == 200
    assert aioclient_mock.call_count == 1
    body = await resp.text()
    assert body == "Frame1Frame2Frame3"


async def test_async_aiohttp_proxy_stream_timeout(
    aioclient_mock: AiohttpClientMocker, camera_client: TestClient
) -> None:
    """Test that it fetches the given url."""
    aioclient_mock.get("http://example.com/mjpeg_stream", exc=TimeoutError())

    resp = await camera_client.get("/api/camera_proxy_stream/camera.mjpeg_camera")
    assert resp.status == 504


async def test_async_aiohttp_proxy_stream_client_err(
    aioclient_mock: AiohttpClientMocker, camera_client: TestClient
) -> None:
    """Test that it fetches the given url."""
    aioclient_mock.get("http://example.com/mjpeg_stream", exc=aiohttp.ClientError())

    resp = await camera_client.get("/api/camera_proxy_stream/camera.mjpeg_camera")
    assert resp.status == 502


async def test_sending_named_tuple(
    hass: SmartHub, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test sending a named tuple in json."""
    resp = aioclient_mock.post("http://127.0.0.1/rgb", json={"rgb": RGBColor(4, 3, 2)})
    session = client.async_create_clientsession(hass)
    resp = await session.post("http://127.0.0.1/rgb", json={"rgb": RGBColor(4, 3, 2)})
    assert resp.status == 200
    assert await resp.json() == {"rgb": [4, 3, 2]}
    assert aioclient_mock.mock_calls[0][2]["rgb"] == RGBColor(4, 3, 2)


async def test_client_session_immutable_headers(hass: SmartHub) -> None:
    """Test we can't mutate headers."""
    session = client.async_get_clientsession(hass)

    with pytest.raises(TypeError):
        session.headers["user-agent"] = "bla"

    with pytest.raises(AttributeError):
        session.headers.update({"user-agent": "bla"})


@pytest.mark.usefixtures("disable_mock_zeroconf_resolver")
@pytest.mark.usefixtures("mock_async_zeroconf")
async def test_async_mdnsresolver(
    hass: SmartHub, aioclient_mock: AiohttpClientMocker
) -> None:
    """Test async_mdnsresolver."""
    resp = aioclient_mock.post("http://localhost/xyz", json={"x": 1})
    session = client.async_create_clientsession(hass)
    resp = await session.post("http://localhost/xyz", json={"x": 1})
    assert resp.status == 200
    assert await resp.json() == {"x": 1}


async def test_resolver_is_singleton(hass: SmartHub) -> None:
    """Test that the resolver is a singleton."""
    session = client.async_get_clientsession(hass)
    session2 = client.async_get_clientsession(hass)
    session3 = client.async_create_clientsession(hass)
    assert isinstance(session._connector, aiohttp.TCPConnector)
    assert isinstance(session2._connector, aiohttp.TCPConnector)
    assert isinstance(session3._connector, aiohttp.TCPConnector)
    assert session._connector._resolver is session2._connector._resolver
    assert session._connector._resolver is session3._connector._resolver
