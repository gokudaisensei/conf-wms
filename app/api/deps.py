import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from pydantic import ValidationError

from app import crud
from app.data import models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

# Other constants
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    """
    Create and return a SQLAlchemy session.

    #### Returns:
        `Session`: The SQLAlchemy session object.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    """
    Get the current user based on the provided token.

    #### Parameters:
        `db`: The SQLAlchemy session.
        `token`: The OAuth2 token.

    #### Returns:
        `models.User`: The current user.

    #### Raises:
        `HTTPException`: If the token is invalid or the user is not found.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    Get the current active user.

    #### Parameters:
        `current_user`: The current user.

    #### Returns:
        `models.User`: The current active user.

    #### Raises:
        `HTTPException`: If the user is not active.
    """
    if not crud.user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="This user is not activated"
        )
    return current_user


def get_if_admin_privileges(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    """
    Get the current user with admin privileges.

    #### Parameters:
        `current_user`: The current user.

    #### Returns:
        `models.User`: The current user with admin privileges.

    #### Raises:
        `HTTPException`: If the user does not have admin privileges.
    """
    if not crud.user.has_admin_privilege(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have admin privileges",
        )
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    """
    Get the current active superuser.

    #### Parameters:
        `current_user`: The current user.

    #### Returns:
        `models.User`: The current active superuser.

    #### Raises:
        `HTTPException`: If the user is not a superuser.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have super admin privileges",
        )
    return current_user
