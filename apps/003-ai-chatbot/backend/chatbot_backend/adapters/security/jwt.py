import os
from datetime import UTC, datetime, timedelta
from typing import Any, cast

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from sqlmodel import Session, select

from chatbot_backend.adapters.db.session import get_session
from chatbot_backend.domain.entities.user import User

# Default secrets for development - should be overridden in .env
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-for-dev")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return str(encoded_jwt)


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return cast(dict[str, Any], payload)
    except JWTError:
        return None


def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
) -> User:
    """Get the current user from the JWT token in cookies."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Get token from cookie
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    user = session.exec(select(User).where(User.id == user_id)).first()
    if user is None:
        raise credentials_exception
    return user
