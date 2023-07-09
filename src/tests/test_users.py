import os
import pytest
from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from app.api.main import app
from app.core.security import create_access_token, get_password_hash
from app.api.deps import get_db
from app import crud
from app import schemas
from app.models import User

from tests.conftest import (
    db_session,
    test_client,
    setup_sadmin,
    TestingSessionLocal,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_read_users(
    test_client: TestClient, db_session: Session, setup_sadmin: schemas.User
):
    # Create test users in the database
    user1 = User(
        name="User 1",
        email="user1@example.com",
        roleID="Admin",
        hashed_password=get_password_hash("pwd1"),
    )
    user2 = User(
        name="User 2",
        email="user2@example.com",
        roleID="Admin",
        hashed_password=get_password_hash("pwd2"),
    )
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    access_token = create_access_token(setup_sadmin.id)

    # Send a GET request to retrieve users
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/users/", headers=headers)
    assert response.status_code == 200

    # Check the response body for the retrieved users
    users = response.json()
    assert len(users) == 3
    assert users[1]["name"] == "User 1"
    assert users[2]["name"] == "User 2"


def test_create_user(
    test_client: TestClient, db_session: Session, setup_sadmin: schemas.User
):
    # Create a user payload
    user_payload = schemas.UserCreate(
        name="New User",
        email="newuser@example.com",
        password="password",
        roleID="Admin",
    )

    access_token = create_access_token(setup_sadmin.id)

    # Extract the password value
    password = user_payload.password.get_secret_value()
    user_payload_dict = user_payload.dict()
    user_payload_dict["password"] = password

    # Send a POST request to create a new user
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/users/", json=user_payload_dict, headers=headers)
    assert response.status_code == 200

    # Check the response body for the created user
    created_user = response.json()
    assert created_user["name"] == "New User"
    assert created_user["email"] == "newuser@example.com"


def test_get_current_user_information(test_client: TestClient, db_session: Session):
    # Create a test user in the database
    user = User(
        name="Test User",
        email="testuser@example.com",
        roleID="Admin",
        enabled=True,
        hashed_password=get_password_hash("pwd1"),
    )
    db_session.add(user)
    db_session.commit()

    # Generate a JWT token for the test user
    access_token = create_access_token(user.id)

    # Send a GET request to get the current user information
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/users/me", headers=headers)
    assert response.status_code == 200

    # Check the response body for the current user information
    current_user = response.json()
    assert current_user["name"] == "Test User"
    assert current_user["email"] == "testuser@example.com"


def test_get_user_by_user_id(test_client: TestClient, db_session: Session):
    # Create a test user in the database
    user = User(
        name="Test User",
        email="testuser@example.com",
        roleID="Admin",
        enabled=True,
        hashed_password=get_password_hash("pwd1"),
    )
    db_session.add(user)
    db_session.commit()
    access_token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}
    # Send a GET request to get the user by ID
    response = test_client.get(f"/users/{user.id}", headers=headers)
    assert response.status_code == 200

    # Check the response body for the retrieved user
    retrieved_user = response.json()
    assert retrieved_user["name"] == "Test User"
    assert retrieved_user["email"] == "testuser@example.com"


def test_update_user(test_client: TestClient, db_session: Session):
    # Create a test user in the database
    user = User(
        name="Test User",
        email="testuser@example.com",
        roleID="Admin",
        enabled=True,
        hashed_password=get_password_hash("pwd1"),
    )
    db_session.add(user)
    db_session.commit()

    # Create an update payload
    update_payload = schemas.UserUpdate(
        name="Updated User", email="updateduser@example.com"
    )

    access_token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {access_token}"}
    # Send a PUT request to update the user
    response = test_client.put(
        f"/users/{user.id}", json=update_payload.dict(), headers=headers
    )
    assert response.status_code == 200

    # Check the response body for the updated user
    updated_user = response.json()
    assert updated_user["name"] == "Updated User"
    assert updated_user["email"] == "updateduser@example.com"


def test_delete_user_by_user_id(
    test_client: TestClient, db_session: Session, setup_sadmin: schemas.User
):
    # Create a test user in the database
    user = User(
        name="Test User",
        email="testuser@example.com",
        roleID="Admin",
        hashed_password=get_password_hash("pwd1"),
    )
    db_session.add(user)
    db_session.commit()

    access_token = create_access_token(setup_sadmin.id)
    # Send a DELETE request to delete the user by ID
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.delete(f"/users/{user.id}", headers=headers)
    assert response.status_code == 200

    # Check the response body for the success message
    success_message = response.json()
    assert success_message["message"] == f"User with ID '{user.id}' has been deleted"


def test_create_user_open(test_client: TestClient, db_session: Session):
    # Create a user payload
    user_payload = {
        "password": "password",
        "email": "newuser@example.com",
        "name": "New User",
    }

    # Send a POST request to create a new user without authentication
    response = test_client.post("/users/open", json=user_payload)
    assert response.status_code == 200

    # Check the response body for the created user
    created_user = response.json()
    assert created_user["name"] == "New User"
    assert created_user["email"] == "newuser@example.com"
