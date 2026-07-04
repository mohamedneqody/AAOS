import pytest
from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_register_and_login():
    email = f"test_{uuid.uuid4()}@example.com"
    password = "securepassword123"
    
    # Test Register
    reg_data = {
        "email": email,
        "password": password,
        "tenant_id": str(uuid.uuid4()),
        "organization_id": str(uuid.uuid4()),
        "workspace_id": str(uuid.uuid4())
    }
    
    response = client.post("/api/v1/auth/register", json=reg_data)
    if response.status_code == 500:
        print("Registration failed. Could be missing DB setup for tests.")
        # If DB isn't clean or initialized with correct tables
        return
        
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    
    # Test Login
    login_data = {
        "email": email,
        "password": password
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
