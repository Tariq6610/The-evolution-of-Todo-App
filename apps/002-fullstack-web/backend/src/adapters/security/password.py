import bcrypt
from passlib.context import CryptContext  # type: ignore[import-untyped]

# Configure CryptContext with options to avoid problematic initialization
# Use bcrypt directly to bypass passlib's problematic initialization
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Set explicit rounds to avoid auto-detection
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    # Ensure password is within bcrypt limits before verification (conservative limit)
    if len(plain_password.encode("utf-8")) > 70:
        # Truncate to 70 bytes for bcrypt compatibility (under 72 for processing)
        truncated_bytes = plain_password.encode("utf-8")[:70]
        plain_password = truncated_bytes.decode("utf-8", errors="ignore")

    # Use bcrypt directly to avoid passlib's problematic initialization
    try:
        # Decode the hashed password if it's in bytes format
        if isinstance(hashed_password, str):
            hashed_bytes = hashed_password.encode("utf-8")
        else:
            hashed_bytes = hashed_password

        if isinstance(plain_password, str):
            plain_bytes = plain_password.encode("utf-8")
        else:
            plain_bytes = plain_password

        result = bcrypt.checkpw(plain_bytes, hashed_bytes)
        return result
    except ValueError as e:
        # Handle bcrypt 72-byte limit error
        if "password cannot be longer than 72 bytes" in str(e):
            # Truncate to 71 bytes just to be safe
            truncated_bytes = plain_password.encode("utf-8")[:71]
            plain_password = truncated_bytes.decode("utf-8", errors="ignore")
            plain_bytes = plain_password.encode("utf-8")
            result = bcrypt.checkpw(plain_bytes, hashed_bytes)
            return result
        else:
            raise


def get_password_hash(password: str) -> str:
    """Generate a hash for a plain password."""
    # Ensure password is within bcrypt limits (conservative limit for variations)
    if len(password.encode("utf-8")) > 70:
        # Truncate to 70 bytes for bcrypt compatibility (under 72 for processing)
        truncated_bytes = password.encode("utf-8")[:70]
        password = truncated_bytes.decode("utf-8", errors="ignore")

    # Use bcrypt directly to avoid passlib's problematic initialization
    try:
        salt = bcrypt.gensalt()
        password_bytes = password.encode("utf-8")
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode("utf-8")
    except ValueError as e:
        # Handle bcrypt 72-byte limit error
        if "password cannot be longer than 72 bytes" in str(e):
            # Truncate to 71 bytes just to be safe
            truncated_bytes = password.encode("utf-8")[:71]
            password = truncated_bytes.decode("utf-8", errors="ignore")
            password_bytes = password.encode("utf-8")
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)
            return hashed.decode("utf-8")
        else:
            raise
