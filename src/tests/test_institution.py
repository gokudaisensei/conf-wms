import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.main import app
from app.core.security import create_access_token, get_password_hash
from app.api.deps import get_db
from app import schemas
from app.models import User, Institution
from tests.conftest import db_session, setup_sadmin, test_client, TestingSessionLocal


def override_get_db():
    db: Session = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_read_all_institution_details(
    test_client: TestClient, db_session: Session, setup_sadmin: schemas.User
):
    # Create test institutions in the database
    institutions_data = [
        {
            "name": "Institution 1",
            "address": "Address 1",
            "email": "institution1@example.com",
            "contactno": "1234567890",
        },
        {
            "name": "Institution 2",
            "address": "Address 2",
            "email": "institution2@example.com",
            "contactno": "9876543210",
        },
        # Add more institutions as needed
    ]
    for institution in institutions_data:
        db_session.add(Institution(**institution))
    db_session.commit()

    access_token = create_access_token(setup_sadmin.id)

    # Send a GET request to retrieve all institutions
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/institutions/", headers=headers)
    assert response.status_code == 200

    # Check the response body for the retrieved institutions
    institutions = response.json()
    assert len(institutions) == 2
    assert institutions[0]["name"] == "Institution 1"
    assert institutions[1]["name"] == "Institution 2"


def test_create_institution(
    test_client: TestClient, db_session: Session, setup_sadmin: schemas.User
):
    # Create an institution payload
    institution_payload = schemas.InstitutionCreate(
        name="New Institution",
        address="New Address",
        email="newemail@example.com",
        contactno="1234567890",
    )

    access_token = create_access_token(setup_sadmin.id)

    # Send a POST request to create a new institution
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post(
        "/institutions/", json=institution_payload.dict(), headers=headers
    )
    assert response.status_code == 200

    # Check the response body for the created institution
    created_institution = response.json()
    assert created_institution["name"] == "New Institution"


def test_get_current_institution_details(
    test_client: TestClient, db_session: Session, setup_sadmin: schemas.User
):
    # Create an institution in the database
    institution = Institution(
        name="Test Institution",
        address="Test Address",
        email="testemail@example.com",
        contactno="9876543210",
    )
    db_session.add(institution)
    db_session.commit()
    db_session.refresh(institution)
    user = User(
        name="Test User",
        email="testuseremail@example.com",
        hashed_password=get_password_hash("pwd1"),
        roleID="Reviewer",
        institution_id=institution.id,
        enabled=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    access_token = create_access_token(user.id)

    # Send a GET request to get the current institution details
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/institutions/me", headers=headers)
    assert response.status_code == 200

    # Check the response body for the current institution details
    current_institution = response.json()
    assert current_institution["name"] == "Test Institution"


def test_read_institution_by_id(
    test_client: TestClient, db_session: Session, setup_sadmin: schemas.User
):
    # Create an institution in the database
    institution = Institution(
        name="Test Institution",
        address="Test Address",
        email="testemail@example.com",
        contactno="9876543210",
    )
    db_session.add(institution)
    db_session.commit()

    access_token = create_access_token(setup_sadmin.id)

    # Send a GET request to get the institution by ID
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get(f"/institutions/{institution.id}", headers=headers)
    assert response.status_code == 200

    # Check the response body for the retrieved institution
    retrieved_institution = response.json()
    assert retrieved_institution["name"] == "Test Institution"


def test_update_institution(
    test_client: TestClient, db_session: Session, setup_sadmin: schemas.User
):
    # Create an institution in the database
    institution = Institution(
        name="Test Institution",
        address="Test Address",
        email="testemail@example.com",
        contactno="9876543210",
    )
    db_session.add(institution)
    db_session.commit()

    # Create an update payload
    update_payload = schemas.InstitutionUpdate(
        name="Updated Institution",
        address="Updated Address",
        email="updatedemail@example.com",
        contactno="1234567890",
    )

    access_token = create_access_token(setup_sadmin.id)

    # Send a PUT request to update the institution
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.put(
        f"/institutions/{institution.id}", json=update_payload.dict(), headers=headers
    )
    assert response.status_code == 200

    # Check the response body for the updated institution
    updated_institution = response.json()
    assert updated_institution["name"] == "Updated Institution"


def test_delete_institution(
    test_client: TestClient, db_session: Session, setup_sadmin: schemas.User
):
    # Create an institution in the database
    institution = Institution(
        name="Test Institution",
        address="Test Address",
        email="testemail@example.com",
        contactno="9876543210",
    )
    db_session.add(institution)
    db_session.commit()

    access_token = create_access_token(setup_sadmin.id)

    # Send a DELETE request to delete the institution
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.delete(f"/institutions/{institution.id}", headers=headers)
    assert response.status_code == 200

    # Check the response body for the success message
    success_message = response.json()
    assert (
        success_message["message"]
        == f"Institution with ID '{institution.id}' has been deleted"
    )
