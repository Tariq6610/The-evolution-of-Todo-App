import os
from collections.abc import Generator
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine


def _load_database_config() -> str:
    """Load database configuration from environment."""
    # Load .env from backend directory (absolute path)
    # session.py is at: backend/src/adapters/db/session.py
    # Need to go up 3 levels to get to backend/: db->adapters->src->backend
    current_file_path = Path(__file__)

    backend_dir = current_file_path.parent.parent.parent  # This should be the backend/ directory
    env_path = backend_dir / ".env"

    # Explicitly load the .env file
    if env_path.exists():
        load_dotenv(env_path, override=True)  # Override any existing env vars
    else:
        # Try alternative locations
        alt_path2 = Path.cwd() / ".env"
        if alt_path2.exists():
            load_dotenv(alt_path2, override=True)

    # Get the database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # Fallback to local sqlite for development if Neon URL is not provided
        database_url = "sqlite:///./todo.db"

    return database_url


# Load the database configuration
DATABASE_URL = _load_database_config()

# For Neon/Postgres, we might need to handle sslmode
if (
    DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://")
) and "sslmode" not in DATABASE_URL:
    connector = "?" if "?" not in DATABASE_URL else "&"
    DATABASE_URL += f"{connector}sslmode=require"

engine = create_engine(DATABASE_URL, echo=True)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
