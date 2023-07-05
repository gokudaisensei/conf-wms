from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.orm import Session
from typing import Any, List
from app import crud
from app.api import deps
from app.core.config import settings
from app.core.security import get_password_hash

from app import schemas, models
from app.api.deps import (
    get_current_user,
    get_db,
    get_pagination_params,
    get_current_active_superuser,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
async def get_current_user_information(
    current_user: schemas.User = Depends(get_current_user),
):
    """
    Get information about the current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, name=name)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by user ID.
    """
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    user = db.query(models.User).filter(models.User.userID == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found.",
        )

    return schemas.User.from_orm(user)


# @router.post("/", response_model=schemas.User)
# async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     """
#     Create a new user.
#     """

#     user.enabled = False  # Set enabled to False for unauthenticated requests
#     user.password = get_password_hash(user.password)
#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return schemas.User.from_orm(new_user)


# @router.delete("/{user_id}")
# async def delete_user_by_user_id(
#     user_id: int,
#     current_user: schemas.User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     """
#     Delete an existing user by user ID.
#     """
#     if current_user.roleID > schemas.RoleEnum.Admin.value:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Insufficient privileges to delete users.",
#         )

#     user = db.query(models.User).filter(models.User.userID == user_id).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with ID '{user_id}' not found.",
#         )

#     db.delete(user)
#     db.commit()

#     return {"message": f"User with ID '{user_id}' has been deleted."}
