import pytest
from fastapi.testclient import TestClient

def test_register_success(client: TestClient):
    """Test successful user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "newuser@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "newuser@example.com"
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate_email(client: TestClient):
    """Test registration with duplicate email fails"""
    # Register first user
    client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    
    # Try to register with same email
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@example.com", "password": "password456"}
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

def test_register_invalid_email(client: TestClient):
    """Test registration with invalid email fails"""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "invalid-email", "password": "password123"}
    )
    assert response.status_code == 422  # Validation error

def test_register_short_password(client: TestClient):
    """Test registration with short password fails"""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "short"}
    )
    assert response.status_code == 422  # Validation error

def test_login_success(client: TestClient):
    """Test successful login"""
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={"email": "logintest@example.com", "password": "testpass123"}
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "logintest@example.com", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "logintest@example.com"
    assert "access_token" in data

def test_login_wrong_password(client: TestClient):
    """Test login with wrong password fails"""
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={"email": "wrongpass@example.com", "password": "correctpass123"}
    )
    
    # Try to login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "wrongpass@example.com", "password": "wrongpass123"}
    )
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()

def test_login_nonexistent_user(client: TestClient):
    """Test login with non-existent email fails"""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@example.com", "password": "anypassword"}
    )
    assert response.status_code == 401

def test_get_current_user_success(client: TestClient, test_user_token: str):
    """Test getting current user with valid token"""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["is_active"] is True

def test_get_current_user_no_token(client: TestClient):
    """Test getting current user without token fails"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 403

def test_get_current_user_invalid_token(client: TestClient):
    """Test getting current user with invalid token fails"""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401
