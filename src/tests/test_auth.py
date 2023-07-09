import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.main import app
from app.core.security import get_password_hash
from app import models
from app.api.deps import get_db

from tests.conftest import TestingSessionLocal, db_session, test_client


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_login_for_access_token(test_client: TestClient, db_session: Session):
    # Insert a test user into the database
    user = models.User(
        email="test@example.com",
        hashed_password=get_password_hash("password"),
        name="Test User",
        enabled=True,
    )
    db_session.add(user)
    db_session.commit()

    # Send a request to the /token endpoint
    response = test_client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "password"},
    )

    # Check the response status code
    assert response.status_code == 200

    # Check the response data
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
