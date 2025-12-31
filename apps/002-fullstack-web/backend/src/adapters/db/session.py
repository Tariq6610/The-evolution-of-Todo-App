from sqlmodel import Session, create_engine, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Fallback to local sqlite for development if Neon URL is not provided
    DATABASE_URL = "sqlite:///./todo.db"

# For Neon/Postgres, we might need to handle sslmode
if DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://"):
    if "sslmode" not in DATABASE_URL:
        connector = "?" if "?" not in DATABASE_URL else "&"
        DATABASE_URL += f"{connector}sslmode=require"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
