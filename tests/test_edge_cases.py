import pytest


def test_signup_nonexistent_activity(client):
    """Test signup for activity that doesn't exist"""
    # Arrange
    email = "test@mergington.edu"
    nonexistent_activity = "NonExistent Club"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_nonexistent_activity(client):
    """Test unregister from activity that doesn't exist"""
    # Arrange
    email = "test@mergington.edu"
    nonexistent_activity = "NonExistent Club"
    
    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_email(client):
    """Test signup when student is already signed up"""
    # Arrange
    email = "duplicate@mergington.edu"
    activity = "Chess Club"
    
    # First signup (setup)
    client.post(
        f"/activities/{activity.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Act - Second signup (should fail)
    response = client.post(
        f"/activities/{activity.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up" in data["detail"]


def test_unregister_not_signed_up(client):
    """Test unregister when student is not signed up"""
    # Arrange
    email = "notsignedup@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not signed up for this activity" in data["detail"]


@pytest.mark.parametrize("activity_name,expected_status", [
    ("Chess Club", 200),
    ("Programming Class", 200),
    ("NonExistent Club", 404),
])
def test_signup_various_activities(client, activity_name, expected_status):
    """Test signup with various activity names"""
    # Arrange
    email = "test@test.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == expected_status


def test_signup_special_characters_in_activity_name(client):
    """Test signup with special characters in activity name"""
    # Arrange
    email = "test@test.edu"
    activity_with_special = "Art & Drama"
    
    # Act
    response = client.post(
        f"/activities/{activity_with_special.replace(' ', '%20').replace('&', '%26')}/signup",
        params={"email": email}
    )
    
    # Assert
    # Should handle URL encoding properly
    assert response.status_code in [200, 404]  # Either succeeds or 404 if activity doesn't exist


def test_signup_missing_email_parameter(client):
    """Test signup without email parameter"""
    # Arrange
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity.replace(' ', '%20')}/signup")
    
    # Assert
    # FastAPI should return 422 for missing required query parameter
    assert response.status_code == 422


def test_unregister_missing_email_parameter(client):
    """Test unregister without email parameter"""
    # Arrange
    activity = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity.replace(' ', '%20')}/signup")
    
    # Assert
    # FastAPI should return 422 for missing required query parameter
    assert response.status_code == 422


def test_signup_empty_email(client):
    """Test signup with empty email"""
    # Arrange
    email = ""
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity.replace(' ', '%20')}/signup",
        params={"email": email}
    )
    
    # Assert
    # Currently no validation, so should succeed
    assert response.status_code == 200


def test_activities_endpoint_not_affected_by_changes(client):
    """Test that GET /activities returns full data regardless of mutations"""
    # Arrange
    email1 = "temp@test.edu"
    email2 = "emma@mergington.edu"
    
    # Act - Make some changes
    client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email1}
    )
    client.delete(
        "/activities/Programming%20Class/signup",
        params={"email": email2}
    )
    
    # Then get activities
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    
    # Should still have all activities
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data
