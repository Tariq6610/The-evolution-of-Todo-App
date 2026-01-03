# Backend: Create Auth

Creates authentication service with JWT token generation, password hashing, and user management.

## Usage

```
/sp.backend.create-auth <AuthServiceName> [--methods "<method1>,<method2>"]
```

## Examples

```bash
# Create AuthService with JWT
/sp.backend.create-auth AuthService --methods "register,login,logout,verify_token,refresh_token"

# Create UserService with auth methods
/sp.backend.create-auth UserService --methods "register,login,logout,change_password,forgot_password"
```

## Auth Creation Rules

1. **File Location**: `apps/002-fullstack-web/backend/app/api/auth.py` or `app/core/auth.py`
2. **JWT Configuration**: Secret keys, algorithm, expiration time
3. **Password Hashing**: bcrypt or argon2 for secure hashing
4. **Token Management**: Access tokens, refresh tokens
5. **Security**: Rate limiting, input validation, SQL injection prevention
6. **Error Handling**: Generic auth errors, don't leak information
7. **Session Management**: Secure storage of user sessions

## Authentication Flow

```python
# Registration
User → Creates Account
     → Hashes password with bcrypt
     → Stores user in database
     → Returns user data (without password hash)

# Login
User → Credentials
     → Validates email and password
     → Verifies password hash
     → Generates JWT access token
     → Generates refresh token
     → Returns tokens

# Token Verification
Request → JWT Token
     → Verifies signature
     → Checks expiration
     → Extracts user ID
     → Returns user data

# Refresh Token
Client → Refresh Token
     → Verifies refresh token
     → Generates new access token
     → Returns new access token
```

## Complete Example: AuthService

```python
# app/core/auth.py
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status

from app.config.settings import (
    JWT_SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from app.db.models import UserModel
from app.db.repositories import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.pwd_context = pwd_context

    async def register(
        self,
        email: str,
        username: str,
        password: str,
    ) -> UserModel:
        """Register new user with hashed password"""
        # Check if user exists
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        # Hash password
        password_hash = self.pwd_context.hash(password)

        # Create user
        user = UserModel(
            email=email,
            username=username,
            password_hash=password_hash,
            is_active=True,
        )

        return await self.user_repo.create(user)

    async def login(
        self,
        email: str,
        password: str,
    ) -> dict:
        """Authenticate user and return JWT tokens"""
        # Get user
        user = await self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled",
            )

        # Verify password
        if not self.pwd_context.verify(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_payload = {
            "sub": str(user.id),
            "exp": datetime.utcnow() + access_token_expires,
        }
        access_token = jwt.encode(
            access_token_payload, JWT_SECRET_KEY, algorithm=ALGORITHM
        )

        # Create refresh token
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token_payload = {
            "sub": str(user.id),
            "exp": datetime.utcnow() + refresh_token_expires,
            "type": "refresh",
        }
        refresh_token = jwt.encode(
            refresh_token_payload, JWT_SECRET_KEY, algorithm=ALGORITHM
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }

    async def verify_token(self, token: str) -> dict:
        """Verify JWT token and return user data"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
            )

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """Use refresh token to get new access token"""
        try:
            payload = jwt.decode(
                refresh_token,
                JWT_SECRET_KEY,
                algorithms=[ALGORITHM],
            )

            # Validate token type
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )

            # Create new access token
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token_payload = {
                "sub": payload["sub"],
                "exp": datetime.utcnow() + access_token_expires,
            }

            access_token = jwt.encode(
                access_token_payload, JWT_SECRET_KEY, algorithm=ALGORITHM
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            }

    async def logout(self, token: str) -> None:
        """Invalidate user session"""
        # In production, blacklist token in Redis
        # For now, just verify and log
        user = await self.verify_token(token)
        self.logger.info(f"User {user['sub']} logged out")
        return None
```

## FastAPI Integration

```python
# app/api/auth.py
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr

from app.core.auth import AuthService
from app.db.session import get_session

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    request: RegisterRequest,
    service: AuthService = Depends(AuthService),
):
    return await service.register(
        email=request.email,
        username=request.username,
        password=request.password,
    )

@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    service: AuthService = Depends(AuthService),
):
    return await service.login(
        email=request.email,
        password=request.password,
    )

@router.post("/refresh")
async def refresh_token(
    refresh_token: str,
    service: AuthService = Depends(AuthService),
):
    return await service.refresh_access_token(refresh_token)

@router.get("/me")
async def get_me(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(AuthService),
):
    return await service.verify_token(token)
```

## Security Best Practices

### Password Hashing

```python
# ✅ Use bcrypt (recommended)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
password_hash = pwd_context.hash(plain_password)

# Verify password
is_valid = pwd_context.verify(plain_password, password_hash)
```

### JWT Configuration

```python
# Environment variables
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Minimum 32 characters
ALGORITHM = "HS256"  # Recommended algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
```

### Token Security

```python
# Include user information
payload = {
    "sub": user_id,        # Subject (user ID)
    "exp": expiration_time,  # Expiration
    "iat": issued_at,        # Issued at
    "role": user_role,      # User role
}

# Sign with secret
token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
```

### Rate Limiting

```python
from slowapi import Limiter

# Rate limiter
limiter = Limiter(key="auth", default_limits=["5 per minute"])

@router.post("/login")
@limiter.limit("5 per minute")
async def login(request: LoginRequest):
    # Implement login logic
```

## Checklist

After creating auth service, verify:
- [ ] Passwords hashed with bcrypt or argon2
- [ ] JWT uses HS256 algorithm
- [ ] Secret keys from environment variables
- [ ] Token expiration configured
- [ ] Access token and refresh token flow
- [ ] Token verification includes expiration check
- [ ] Generic error messages (no user existence info)
- [ ] Rate limiting implemented
- [ ] Input validation (email format, password strength)
- [ ] SQL injection prevented
- [ ] Session management (logout/blacklist)
- [ ] HTTPS required in production
- [ ] CORS configured properly
- [ ] Security headers set
