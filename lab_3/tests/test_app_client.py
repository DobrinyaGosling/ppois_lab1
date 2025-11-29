import asyncio
import json

from fastapi.testclient import TestClient

from src.errors import GalleryBaseError
from src.presentation.api.app import handle_domain_error


def test_client_fixture_initializes_fastapi_app(client: TestClient) -> None:
    assert client.app.title == "Gallery API"


def test_exception_handler_maps_domain_errors() -> None:
    exc = GalleryBaseError(error_code="E42", message="boom")
    response = asyncio.run(handle_domain_error(None, exc))
    assert response.status_code == 400
    payload = json.loads(response.body)
    assert payload["detail"].startswith("E42")
