"""Tests for POST /activities/{activity_name}/signup endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_signup_with_valid_activity_and_email_returns_200(client):
    """Test that signup with valid activity and email returns 200 status"""
    # Arrange
    activity_name = "Art Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200


def test_signup_returns_success_message(client):
    """Test that signup returns a success message"""
    # Arrange
    activity_name = "Drama Club"
    email = "actor@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    result = response.json()

    # Assert
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]


def test_signup_adds_student_to_participants(client):
    """Test that signup actually adds the student to the participants list"""
    # Arrange
    activity_name = "Math Olympiad"
    email = "mathgenius@mergington.edu"

    # Act
    client.post(f"/activities/{activity_name}/signup?email={email}")
    activities_response = client.get("/activities")
    activities = activities_response.json()

    # Assert
    assert email in activities[activity_name]["participants"]


def test_signup_increases_participant_count(client):
    """Test that signup increases the participant count for an activity"""
    # Arrange
    activity_name = "Science Club"
    email = "scientist@mergington.edu"

    # Act - get initial count
    initial_response = client.get("/activities")
    initial_activities = initial_response.json()
    initial_count = len(initial_activities[activity_name]["participants"])

    # Act - signup
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act - get new count
    updated_response = client.get("/activities")
    updated_activities = updated_response.json()
    updated_count = len(updated_activities[activity_name]["participants"])

    # Assert
    assert updated_count == initial_count + 1
