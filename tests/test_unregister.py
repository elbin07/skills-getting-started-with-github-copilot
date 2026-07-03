"""Tests for POST /activities/{activity_name}/unregister endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_unregister_existing_participant_returns_200(client):
    """Test that unregistering an existing participant returns 200 status"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already enrolled in Chess Club

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    # Assert
    assert response.status_code == 200


def test_unregister_returns_success_message(client):
    """Test that unregister returns a success message"""
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already enrolled in Programming Class

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    result = response.json()

    # Assert
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]


def test_unregister_removes_student_from_participants(client):
    """Test that unregister actually removes the student from the participants list"""
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"  # Already enrolled in Gym Class

    # Act
    client.post(f"/activities/{activity_name}/unregister?email={email}")
    activities_response = client.get("/activities")
    activities = activities_response.json()

    # Assert
    assert email not in activities[activity_name]["participants"]


def test_unregister_decreases_participant_count(client):
    """Test that unregister decreases the participant count for an activity"""
    # Arrange
    activity_name = "Soccer Team"
    email = "nina@mergington.edu"  # Already enrolled in Soccer Team

    # Act - get initial count
    initial_response = client.get("/activities")
    initial_activities = initial_response.json()
    initial_count = len(initial_activities[activity_name]["participants"])

    # Act - unregister
    client.post(f"/activities/{activity_name}/unregister?email={email}")

    # Act - get new count
    updated_response = client.get("/activities")
    updated_activities = updated_response.json()
    updated_count = len(updated_activities[activity_name]["participants"])

    # Assert
    assert updated_count == initial_count - 1
