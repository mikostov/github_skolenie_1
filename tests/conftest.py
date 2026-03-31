import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the original activities state
ORIGINAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test"""
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    yield


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app"""
    return TestClient(app, follow_redirects=False)
