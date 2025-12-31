from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from src.domain.entities.user import User, UserCreate
from src.domain.services.auth_service import AuthService
from src.adapters.db.user_repository import SQLUserRepository
from src.adapters.db.session import get_session
from sqlmodel import Session

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
def register(user_in: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    try:
        user = auth_service.register(user_in)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    try:
        user = auth_service.authenticate(form_data.username, form_data.password)
        token_data = auth_service.create_token(user)
        return token_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )