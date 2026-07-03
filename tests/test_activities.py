"""Tests for the GET /activities endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_get_activities_returns_200_status(client):
    """Test that GET /activities returns a 200 status code"""
    # Arrange
    # (client fixture is already set up)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200


def test_get_activities_returns_dict_of_activities(client):
    """Test that GET /activities returns a dictionary of activities"""
    # Arrange
    # (client fixture is already set up)

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_get_activities_contains_expected_activity_names(client):
    """Test that GET /activities includes expected activity names"""
    # Arrange
    expected_activities = {"Chess Club", "Programming Class", "Gym Class", "Soccer Team", "Swimming Club"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    returned_names = set(activities.keys())
    assert expected_activities.issubset(returned_names)


def test_activity_has_required_fields(client):
    """Test that each activity has all required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()
    first_activity = next(iter(activities.values()))

    # Assert
    assert all(field in first_activity for field in required_fields)


def test_activity_participants_is_list(client):
    """Test that participants field is a list"""
    # Arrange
    # (client fixture is already set up)

    # Act
    response = client.get("/activities")
    activities = response.json()
    first_activity = next(iter(activities.values()))

    # Assert
    assert isinstance(first_activity["participants"], list)
