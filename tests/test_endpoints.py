import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities"""
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Current number of activities
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_get_activities_returns_correct_structure(client):
    """Test that activities have the correct structure"""
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_root_redirect_to_static(client):
    """Test that GET / redirects to static/index.html"""
    # Arrange - No special setup needed
    
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"


def test_signup_new_student(client):
    """Test successful signup of a new student"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity}" in data["message"]


def test_signup_updates_participants_list(client):
    """Test that signup actually adds to participants list"""
    # Arrange
    email = "test@mergington.edu"
    activity = "Chess Club"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    initial_count = len(initial_data[activity]["participants"])
    
    # Act
    client.post(
        f"/activities/{activity.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Assert
    response = client.get("/activities")
    updated_data = response.json()
    updated_count = len(updated_data[activity]["participants"])
    assert updated_count == initial_count + 1
    assert email in updated_data[activity]["participants"]


def test_unregister_existing_student(client):
    """Test successful unregistration of an existing student"""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Unregistered {email} from {activity}" in data["message"]


def test_unregister_updates_participants_list(client):
    """Test that unregister actually removes from participants list"""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    initial_count = len(initial_data[activity]["participants"])
    
    # Act
    client.delete(
        f"/activities/{activity.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Assert
    response = client.get("/activities")
    updated_data = response.json()
    updated_count = len(updated_data[activity]["participants"])
    assert updated_count == initial_count - 1
    assert email not in updated_data[activity]["participants"]
