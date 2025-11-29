import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client() -> TestClient:
    """Provide a fresh FastAPI test client with reset state."""
    from src.presentation import dependencies
    from src.presentation.api.app import app

    dependencies.reset_state()
    return TestClient(app)
