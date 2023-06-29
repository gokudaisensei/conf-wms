import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.data import models, schemas
from app.dependencies import get_db
from random import choice

from tests import create_users, ROLE_ENUM

# Create an in-memory SQLite database for testing
engine = create_engine(os.getenv('TESTING_DATABASE_URL'))  # type: ignore
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def db_session():
    # Create the test database tables
    models.Base.metadata.create_all(bind=engine)

    # Set up a test database session
    session = TestingSessionLocal()

    yield session

    # Clean up the test database tables
    models.Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_get_all_users_by_role(test_client: TestClient, db_session: Session):
    # Insert some test data into the database
    user_count = 3
    for role in ROLE_ENUM.keys():
        users = create_users(role, count=user_count)
        for user in users:
            db_session.add(models.User(**user))
        db_session.commit()

    # Send a request to the API endpoint
    response = test_client.get(
        "/users", params={"role_name": 'Admin'})

    # Check the response status code
    assert response.status_code == 200

    # Check the response data
    data = response.json()
    assert len(data) == user_count
    assert data[0]["name"] == "Admin 1"
    assert data[0]["roleID"] == "Admin"

    # Clean up the test data from the database
    db_session.query(models.User).delete()
    db_session.commit()


def test_get_all_users_without_role(test_client: TestClient, db_session: Session):
    # Insert some test data into the database
    user_count = 3
    for role in ROLE_ENUM.keys():
        users = create_users(role, count=user_count)
        for user in users:
            db_session.add(models.User(**user))
        db_session.commit()

    # Send a request to the API endpoint
    response = test_client.get(
        "/users")

    # Check the response status code
    assert response.status_code == 200

    # Check the response data
    data = response.json()
    # Using value 10 because of pagination limit per page by default is 10
    assert len(data) == 10

    # Clean up the test data from the database
    db_session.query(models.User).delete()
    db_session.commit()


def test_get_user_by_user_id(test_client: TestClient, db_session: Session):
    # Insert some test data into the database
    user_count = 3
    for role in ROLE_ENUM.keys():
        users = create_users(role, count=user_count)
        for user in users:
            db_session.add(models.User(**user))
        db_session.commit()

    queried_user = choice(db_session.query(models.User).all())
    test_user_id = queried_user.userID

    # Send a request to the API endpoint with the obtained userID
    response = test_client.get(f'/users/{test_user_id}')

    # Check the response status code
    assert response.status_code == 200

    # Check the response data
    data = response.json()
    # Checking if the number of fields retrieved is 6
    assert len(data) == 6

    # Clean up the test data from the database
    db_session.query(models.User).delete()
    db_session.commit()
