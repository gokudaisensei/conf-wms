from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
from typing import Any, List

from app import crud
from app.core.config import settings
from app import schemas, models
from app.api.deps import (
    get_current_user,
    get_db,
    get_current_active_superuser,
    get_if_admin_privileges,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[schemas.User], summary="Retrieve users")
def read_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, gt=0),
    sadmin: models.User = Depends(get_current_active_superuser),
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User, summary="Create new user")
async def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_superuser),
) -> Any:
    if crud.user.get_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    user_in.enabled = True
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get(
    "/me", response_model=schemas.User, summary="Get information about the current user"
)
def get_current_user_information(
    current_user: schemas.User = Depends(get_current_user),
):
    return current_user


@router.get("/{user_id}", response_model=schemas.User, summary="Get a user by user ID")
async def get_user_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_if_admin_privileges),
) -> Any:
    if not (user := crud.user.get(db, id=user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return user


@router.put("/{user_id}", response_model=schemas.User, summary="Update a user")
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_if_admin_privileges),
) -> Any:
    if not (user := crud.user.get(db, id=user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", summary="Delete an existing user by user ID")
async def delete_user_by_user_id(
    user_id: int,
    db: Session = Depends(get_db),
    admin: schemas.User = Depends(get_if_admin_privileges),
):
    if user_id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Deletion of self not allowed.",
        )
    if not crud.user.remove(db, id=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} does not exist",
        )

    return {"message": f"User with ID '{user_id}' has been deleted"}


@router.post(
    "/open",
    response_model=schemas.User,
    summary="Create new user without the need to be logged in",
)
def create_user_open(
    password: str = Body(...),
    email: EmailStr = Body(...),
    name: str = Body(...),
    institution_id: int = Body(None),
    db: Session = Depends(get_db),
) -> Any:
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(
        password=password,
        email=email,
        name=name,
        institutionID=institution_id,
        enabled=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    return user
