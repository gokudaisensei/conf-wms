from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.data import schemas, models
from app.dependencies import get_current_user, get_db, get_pagination_params, get_password_hash

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.get('/', response_model=List[schemas.User])
async def get_all_users_by_role(
    role_name: schemas.RoleEnum = None,
    pagination: dict = Depends(get_pagination_params),
    db: Session = Depends(get_db)
):
    """
    Get all users filtered by role.
    """
    offset = (pagination['page'] - 1) * pagination['per_page']
    query = db.query(models.User)

    if role_name:
        query = query.filter(models.User.roleID == role_name)

    users = query.offset(offset).limit(pagination['per_page']).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Users not found.")

    return [schemas.User.from_orm(user) for user in users]


@router.get("/me", response_model=schemas.User)
async def get_current_user_information(
    current_user: schemas.User = Depends(get_current_user)
):
    """
    Get information about the current user.
    """
    return current_user


@router.get('/{user_id}', response_model=schemas.User)
async def get_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by user ID.
    """
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    user = db.query(models.User).filter(models.User.userID == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID '{user_id}' not found.")

    return schemas.User.from_orm(user)


@router.post("/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user.
    """

    user.enabled = False  # Set enabled to False for unauthenticated requests
    user.password = get_password_hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return schemas.User.from_orm(new_user)


@router.delete("/{user_id}")
async def delete_user_by_user_id(
    user_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an existing user by user ID.
    """
    if current_user.roleID > schemas.RoleEnum.Admin.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient privileges to delete users."
        )

    user = db.query(models.User).filter(models.User.userID == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID '{user_id}' not found.")

    db.delete(user)
    db.commit()

    return {"message": f"User with ID '{user_id}' has been deleted."}
