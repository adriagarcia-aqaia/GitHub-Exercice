from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    """Create a FastAPI test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activity data before each test for isolation."""
    snapshot = deepcopy(activities)
    yield
    activities.clear()
    activities.update(snapshot)
