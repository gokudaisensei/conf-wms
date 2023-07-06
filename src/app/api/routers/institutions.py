from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Any, List

from app import crud, schemas
from app.api.deps import (
    get_current_active_user,
    get_db,
    get_current_active_superuser,
    get_if_admin_privileges,
)

router = APIRouter(prefix="/institutions", tags=["institution"])


@router.get(
    "/", response_model=List[schemas.Institution], summary="Get all Institutions"
)
def read_all_institution_details(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    superadmin: schemas.User = Depends(get_current_active_superuser),
) -> Any:
    institutions = crud.institution.get_multi(db, skip=skip, limit=limit)
    return institutions


@router.post("/", response_model=schemas.Institution, summary="Create an Institution")
def create_institution(
    db: Session = Depends(get_db),
    *,
    sadmin: schemas.User = Depends(get_current_active_superuser),
    institution_in: schemas.InstitutionCreate,
) -> Any:
    if crud.institution.get_by_name(db, name=institution_in.name) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Institution with this name already exists",
        )
    institution = crud.institution.create(db, obj_in=institution_in)
    return institution


@router.get(
    "/me",
    response_model=schemas.Institution,
    summary="Get the currently logged-in user's Institution details",
)
def get_current_institution_details(
    *,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
) -> Any:
    if current_user.institution is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user is not assigned to an institution.",
        )
    return schemas.Institution.from_orm(current_user.institution)


@router.get(
    "/{institution_id}",
    response_model=schemas.Institution,
    summary="Get Institution by ID",
)
def read_institution_by_id(
    db: Session = Depends(get_db),
    *,
    institution_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
) -> Any:
    if not (institution := crud.institution.get(db, id=institution_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Institution with ID {institution_id} was not found",
        )
    return institution


@router.get(
    "/{institution_id}/users",
    response_model=List[schemas.User],
    summary="Get all Users associated to a particular Institution",
)
def read_all_users_of_institution(
    *,
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_if_admin_privileges),
    institution_id: int,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return crud.institution.get_multi_user(
        db, id=institution_id, skip=skip, limit=limit
    )


@router.put(
    "/{institution_id}",
    response_model=schemas.Institution,
    summary="Update an existing Institution.",
)
def update_institution(
    *,
    institution_id: int,
    institution_in: schemas.InstitutionUpdate,
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_if_admin_privileges),
) -> Any:
    if not (institution := crud.user.get(db, id=institution_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    institution_update = crud.user.update(db, db_obj=institution, obj_in=institution_in)
    return institution_update


@router.delete("/{institution_id}", summary="Delete an existing Institution by its ID")
def delete_institution(
    *,
    institution_id: int,
    db: Session = Depends(get_db),
    sadmin: schemas.User = Depends(get_current_active_superuser),
) -> Any:
    if not crud.institution.remove(db, id=institution_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {institution_id} does not exist",
        )

    return {"message": f"User with ID '{institution_id}' has been deleted"}
