import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.data import models
from app.main import app

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