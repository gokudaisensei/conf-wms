from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the plain password matches the hashed password.

    #### Parameters:
        * `plain_password`: The plain password to verify.
        * `hashed_password`: The hashed password to compare against.

    #### Returns:
        `bool`: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for the given password.

    #### Parameters:
        `password`: The password to hash.

    #### Returns:
        `str`: The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(subject: str | Any, expires_delta: timedelta = None) -> str:
    """
    Create an access token.

    #### Parameters:
        * `subject`: The subject of the token.
        * `expires_delta`: The expiration delta. Defaults to None.

    #### Returns:
        `str`: The access token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
