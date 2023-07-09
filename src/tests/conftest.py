import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app import models

from app.db.base import Base
from app.api.main import app
from app.core.config import settings
from app.db.init_db import init_db

engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URI)
TestingSessionLocal: Session = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def db_session():
    # Create the test database tables
    Base.metadata.create_all(bind=engine)

    # Set up a test database session
    session = TestingSessionLocal()

    yield session

    # Clean up the test database tables
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_sadmin(db_session: Session):
    init_db(db_session)
    sadmin = db_session.query(models.User).first()
    yield sadmin
    metadata = Base.metadata
    for table in reversed(metadata.sorted_tables):
        db_session.execute(table.delete())

    db_session.commit()
