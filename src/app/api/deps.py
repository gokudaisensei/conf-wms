import os
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from pydantic import ValidationError

from app.data import models, schemas
from app.core.config import settings
from app.core import security
from app import crud
from app.db.session import SessionLocal

# Other constants
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    """Create and return a SQLAlchemy session.

    Returns:
        Session: The SQLAlchemy session object.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_pagination_params(page: int = Query(1, gt=0), per_page: int = Query(10, gt=0)):
    """Get pagination parameters.

    Args:
        page (int, optional): Page number. Defaults to 1.
        per_page (int, optional): Number of items per page. Defaults to 10.

    Returns:
        dict: Pagination parameters (page and per_page).
    """
    return {"page": page, "per_page": per_page}


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
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


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return current_user
