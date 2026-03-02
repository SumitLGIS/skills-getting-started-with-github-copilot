from urllib.parse import quote


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/participants"

    # Act
    unregister_response = client.delete(endpoint, params={"email": email})
    activities_response = client.get("/activities")

    # Assert
    assert unregister_response.status_code == 200
    assert "Unregistered" in unregister_response.json()["message"]
    assert email not in activities_response.json()[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    endpoint = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(endpoint, params={"email": "student@mergington.edu"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_participant_not_in_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "absent@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(endpoint, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_returns_422_when_email_is_missing(client):
    # Arrange
    activity_name = "Chess Club"
    endpoint = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(endpoint)

    # Assert
    assert response.status_code == 422
    error_details = response.json()["detail"]
    assert isinstance(error_details, list)
    assert any(item.get("loc") == ["query", "email"] for item in error_details)
