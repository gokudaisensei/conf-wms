from fastapi import APIRouter, Depends, HTTPException, status
from app.data import schemas, models
from app.dependencies import get_current_user, get_db, get_pagination_params
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/', response_model=list[schemas.User])
async def get_all_users_by_role(
    role_name: schemas.RoleEnum | None = None,
    pagination: dict = Depends(get_pagination_params),
    db: Session = Depends(get_db)
):
    offset = (pagination['page'] - 1) * pagination['per_page']
    if role_name is not None:
        users = db.query(models.User).filter(models.User.roleID == role_name).offset(
            offset).limit(pagination['per_page']).all()
    else:
        users = db.query(models.User).offset(
            offset).limit(pagination['per_page']).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Users not found.")

    return [schemas.User.from_orm(user) for user in users]


@router.get("/me", response_model=schemas.User)
async def get_current_user_information(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    return current_user


@router.get('/{user_id}', response_model=schemas.User)
async def get_user_by_user_id(user_id: int, db: Session = Depends(get_db)):
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    user = db.query(models.User).filter(models.User.userID == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User with ID '{user_id}' not found.")
    return schemas.User.from_orm(user)
