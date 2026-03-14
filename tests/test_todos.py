import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta

def test_create_todo_success(client: TestClient, test_user_token: str):
    """Test creating a todo successfully"""
    response = client.post(
        "/api/v1/todos",
        json={
            "title": "Test Todo",
            "description": "Test description",
            "is_done": False,
            "due_date": "2026-03-20",
            "tags": ["learn", "python"]
        },
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test description"
    assert data["is_done"] is False
    assert data["due_date"] == "2026-03-20"
    assert len(data["tags"]) == 2
    assert "id" in data
    assert "created_at" in data

def test_create_todo_short_title(client: TestClient, test_user_token: str):
    """Test creating a todo with short title fails"""
    response = client.post(
        "/api/v1/todos",
        json={
            "title": "ab",  # Less than 3 chars
            "description": "Test"
        },
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 422

def test_create_todo_missing_title(client: TestClient, test_user_token: str):
    """Test creating a todo without title fails"""
    response = client.post(
        "/api/v1/todos",
        json={"description": "Test"},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 422

def test_create_todo_no_auth(client: TestClient):
    """Test creating a todo without auth fails"""
    response = client.post(
        "/api/v1/todos",
        json={"title": "Test Todo"}
    )
    assert response.status_code == 403

def test_get_todos_list(client: TestClient, test_user_token: str):
    """Test getting todos list"""
    # Create a todo
    client.post(
        "/api/v1/todos",
        json={"title": "Todo 1", "tags": ["work"]},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    # Get todos
    response = client.get(
        "/api/v1/todos",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data
    assert len(data["items"]) == 1
    assert data["total"] == 1

def test_get_todo_by_id_success(client: TestClient, test_user_token: str):
    """Test getting a specific todo by ID"""
    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "Get Me", "description": "Find me"},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    todo_id = create_response.json()["id"]
    
    # Get todo by ID
    response = client.get(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Get Me"

def test_get_todo_by_id_not_found(client: TestClient, test_user_token: str):
    """Test getting a non-existent todo fails"""
    response = client.get(
        "/api/v1/todos/9999",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 404

def test_update_todo_success(client: TestClient, test_user_token: str):
    """Test updating a todo"""
    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "Old Title", "is_done": False},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    todo_id = create_response.json()["id"]
    
    # Update todo
    response = client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "New Title", "is_done": True, "tags": ["updated"]},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["is_done"] is True
    assert len(data["tags"]) == 1

def test_partial_update_todo(client: TestClient, test_user_token: str):
    """Test partial update (PATCH) of a todo"""
    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "Original", "description": "Original desc"},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    todo_id = create_response.json()["id"]
    
    # Partial update - only update title
    response = client.patch(
        f"/api/v1/todos/{todo_id}",
        json={"title": "Updated Title"},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Original desc"

def test_delete_todo_success(client: TestClient, test_user_token: str):
    """Test deleting a todo"""
    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "Delete Me"},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    todo_id = create_response.json()["id"]
    
    # Delete todo
    response = client.delete(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(
        f"/api/v1/todos/{todo_id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert get_response.status_code == 404

def test_delete_todo_not_found(client: TestClient, test_user_token: str):
    """Test deleting a non-existent todo fails"""
    response = client.delete(
        "/api/v1/todos/9999",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 404

def test_complete_todo(client: TestClient, test_user_token: str):
    """Test marking a todo as complete"""
    # Create a todo
    create_response = client.post(
        "/api/v1/todos",
        json={"title": "Complete Me", "is_done": False},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    todo_id = create_response.json()["id"]
    
    # Complete todo
    response = client.post(
        f"/api/v1/todos/{todo_id}/complete",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_done"] is True

def test_get_overdue_todos(client: TestClient, test_user_token: str):
    """Test getting overdue todos"""
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    
    # Create an overdue todo
    client.post(
        "/api/v1/todos",
        json={"title": "Overdue", "due_date": yesterday},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    # Get overdue todos
    response = client.get(
        "/api/v1/todos/overdue/list",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1

def test_get_today_todos(client: TestClient, test_user_token: str):
    """Test getting today's todos"""
    today = date.today().isoformat()
    
    # Create a todo for today
    client.post(
        "/api/v1/todos",
        json={"title": "Today", "due_date": today},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    
    # Get today's todos
    response = client.get(
        "/api/v1/todos/today/list",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert len(data["items"]) == 1

def test_multi_user_isolation(client: TestClient):
    """Test that users can only see their own todos"""
    # Register user 1
    response1 = client.post(
        "/api/v1/auth/register",
        json={"email": "user1@test.com", "password": "pass123"}
    )
    token1 = response1.json()["access_token"]
    
    # Register user 2
    response2 = client.post(
        "/api/v1/auth/register",
        json={"email": "user2@test.com", "password": "pass123"}
    )
    token2 = response2.json()["access_token"]
    
    # User 1 creates a todo
    user1_todo = client.post(
        "/api/v1/todos",
        json={"title": "User1 Todo"},
        headers={"Authorization": f"Bearer {token1}"}
    ).json()
    
    # User 2 should not be able to access user 1's todo
    response = client.get(
        f"/api/v1/todos/{user1_todo['id']}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 404
    
    # User 1 should be able to access their own todo
    response = client.get(
        f"/api/v1/todos/{user1_todo['id']}",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 200
