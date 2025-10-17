from fastapi.testclient import TestClient
import pytest

def test_get_activities(client):
    """Test getting the list of activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    # Check for some known activities
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()

def test_signup_new_participant(client):
    """Test signing up a new participant for an activity"""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify the participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate_participant(client):
    """Test that a participant cannot sign up twice"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Using existing participant
    
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    response = client.post("/activities/NonExistentClub/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_unregister_participant(client):
    """Test unregistering a participant from an activity"""
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"  # Using existing participant
    
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    
    # Verify the participant was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_nonregistered_participant(client):
    """Test unregistering a participant who is not registered"""
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"
    
    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()

def test_unregister_from_nonexistent_activity(client):
    """Test unregistering from a non-existent activity"""
    response = client.delete("/activities/NonExistentClub/unregister", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()