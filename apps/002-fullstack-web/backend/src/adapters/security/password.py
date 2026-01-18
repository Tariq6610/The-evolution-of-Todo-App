from passlib.context import CryptContext  # type: ignore[import-untyped]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    # Ensure password is within bcrypt limits before verification
    if len(plain_password.encode("utf-8")) > 72:
        # Truncate to 72 bytes for bcrypt compatibility
        truncated_bytes = plain_password.encode("utf-8")[:72]
        plain_password = truncated_bytes.decode("utf-8", errors="ignore")
    result = pwd_context.verify(plain_password, hashed_password)
    return bool(result)


def get_password_hash(password: str) -> str:
    """Generate a hash for a plain password."""
    # Ensure password is within bcrypt limits (72 bytes)
    if len(password.encode("utf-8")) > 72:
        # Truncate to 72 bytes for bcrypt compatibility
        truncated_bytes = password.encode("utf-8")[:72]
        password = truncated_bytes.decode("utf-8", errors="ignore")
    result = pwd_context.hash(password)
    return str(result)
