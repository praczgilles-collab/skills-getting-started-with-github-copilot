import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    # Test signup
    email = "testuser@example.com"
    activity = "Basketball Team"
    # Remove if already present
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Vérifier que l'email est bien inscrit
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # Unregister
    print("Participants avant désinscription:", client.get("/activities").json()[activity]["participants"])
    response3 = client.post(f"/activities/{activity}/unregister?email={email}")
    print("Réponse désinscription:", response3.status_code, response3.json())
    assert response3.status_code == 200
    # Vérifier que l'email n'est plus inscrit
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
    # Unregister again should fail
    response4 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response4.status_code == 404
