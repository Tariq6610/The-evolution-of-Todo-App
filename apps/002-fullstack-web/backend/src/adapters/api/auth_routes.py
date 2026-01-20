from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from src.domain.entities.user import User, UserCreate
from src.domain.services.auth_service import AuthService
from src.adapters.db.user_repository import SQLUserRepository
from src.adapters.db.session import get_session
from src.adapters.security.jwt import get_current_user
from sqlmodel import Session
from fastapi.responses import JSONResponse
from fastapi import Request

router = APIRouter(tags=["Authentication"])


# Request/Response models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True


# Dependency to get auth service
def get_auth_service(session: Session = Depends(get_session)) -> AuthService:
    user_repo = SQLUserRepository(session)
    return AuthService(user_repo)


@router.post("/register", response_model=UserResponse)
def register(
    user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    try:
        user = auth_service.register(user_in)
        # Convert User entity to UserResponse model
        return UserResponse(
            id=user.id or "",
            email=user.email,
            full_name=user.full_name or "",
            is_active=user.is_active
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> JSONResponse:
    try:
        user = auth_service.authenticate(form_data.username, form_data.password)
        token_data = auth_service.create_token(user)
        access_token = token_data["access_token"]  # Dict access, not attribute

        # Create response with token in both response body and cookie
        response = JSONResponse(
            content={
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user.id,
                "email": user.email,
            }
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,  # Prevent XSS attacks
            secure=True,  # Required for HTTPS in production
            samesite="none",  # Required for cross-origin requests (frontend/backend on different domains)
            max_age=1800,  # 30 minutes expiry
            path="/",  # Make cookie available for all routes
            domain=None,  # Use this to allow cookie to be sent with cross-origin requests
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/logout")
def logout() -> JSONResponse:
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie("access_token", path="/", domain=None)
    return response


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Get current authenticated user."""
    # Convert User entity to UserResponse model
    return UserResponse(
        id=current_user.id or "",
        email=current_user.email,
        full_name=current_user.full_name or "",
        is_active=current_user.is_active
    )
