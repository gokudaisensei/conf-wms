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

from app.data import models, schemas

# Other constants
SECRET_KEY = "dd6b67df34bc60725b707ac970c6e2cab74f7b01a1523d4266b7c6c8915c2a28"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    """Create and return a SQLAlchemy session.

    Returns:
        Session: The SQLAlchemy session object.
    """
    # Set up SQLAlchemy session
    engine = create_engine(os.getenv("DATABASE_URL"))  # type: ignore
    local_session = sessionmaker(
        autocommit=False, autoflush=False, bind=engine)
    db = local_session()
    try:
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


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the plain password matches the hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a hash for the given password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def get_user(db: Session, email: str):
    """Retrieve a user from the database by email.

    Args:
        db (Session): The SQLAlchemy session.
        email (str): The email of the user to retrieve.

    Returns:
        models.User: The user object if found, None otherwise.
    Raises:
        HTTPException: If there is an error retrieving the user.
    """
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        return user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


def authenticate_user(db: Session, email: str, password: str):
    """Authenticate a user with the given email and password.

    Args:
        db (Session): The SQLAlchemy session.
        email (str): The email of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        models.User | bool: The authenticated user if successful, False otherwise.
    """
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create an access token with the provided data.

    Args:
        data (dict): The data to include in the access token.
        expires_delta (timedelta | None, optional): The expiration time delta. Defaults to None.

    Returns:
        str: The generated access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db=Depends(get_db)):
    """Retrieve the current user based on the provided access token.

    Args:
        token (str): The access token for authentication.
        db (Session, optional): The SQLAlchemy session. Defaults to Depends(get_db).

    Returns:
        schemas.User: The authenticated user.

    Raises:
        HTTPException: If the credentials cannot be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # type: ignore
        if email is None:
            raise credentials_exception
        user = get_user(db, email)
        if user is None:
            raise credentials_exception
        return schemas.User.from_orm(user)
    except JWTError:
        raise credentials_exception
