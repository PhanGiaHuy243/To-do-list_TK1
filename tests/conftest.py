import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import httpx
from httpx._transports.asgi import ASGITransport
from app.core.database import Base
from app.core.models import UserModel, TodoModel, TagModel
from app.core.security import hash_password
from main import app
from app.core.database import get_db
import asyncio

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        database = TestingSessionLocal()
        try:
            yield database
        finally:
            database.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal()
    
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def client(db):
    """Create a test client using httpx with ASGI transport"""
    transport = ASGITransport(app=app)
    with httpx.Client(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="function")
def test_user(db):
    """Create a test user"""
    user = UserModel(
        email="test@example.com",
        hashed_password=hash_password("testpassword123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(scope="function")
def test_user_token(db, client):
    """Get JWT token for test user"""
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "testuser@example.com", "password": "testpass123"}
    )
    return response.json()["access_token"]
