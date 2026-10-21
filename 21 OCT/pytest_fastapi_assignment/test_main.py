from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_get_task():
    response = client.get("/tasks")
    assert response.status_code == 200

def test_get_task_id():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_invalid_id():
    response = client.get( "/tasks/999")
    assert response.status_code == 404

def test_add_task():
    response = client.post(
        "/tasks",
    json={
            "id": 4,
            "title": "Check server logs",
            "status": "Pending"
            })
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 4
    assert data["title"] == "Check server logs"
    assert data["status"] == "Pending"

def test_invalid_data():
    response = client.post(
        "/tasks",
    json={"title": "Check server logs", "status": "Pending"}
    )
    assert response.status_code == 422

def test_update_task():
    response = client.put("/tasks/1", json={"id":1,"title": "Prepare report", "status": "Completed"})
    assert response.status_code == 200

def test_delete_task():
    response = client.delete("/tasks/3")
    assert response.status_code == 200

def test_check_delete_task():
    response = client.get("/tasks/3")
    assert response.status_code == 404

#commands used
#pytest
#python -m pytest -v




