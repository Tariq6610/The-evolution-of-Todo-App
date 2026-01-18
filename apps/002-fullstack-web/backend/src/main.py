import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.api import auth_routes, task_routes  # type: ignore
from src.adapters.db.session import init_db  # type: ignore

app = FastAPI(
    title="Todo Evolution API",
    description="Full-stack Todo application backend for Phase II",
    version="0.1.0",
)

# Configure CORS
# Note: When using credentials (cookies), origins must be specific, not "*"
ALLOWED_ORIGINS: list[str] = [
    "http://localhost:3000",  # Next.js frontend
    "http://127.0.0.1:3000",
    "https://the-evolution-of-todo-app-production.up.railway.app",  # Deployed frontend
    "https://frontend-orpin-seven-86.vercel.app",  # Vercel deployed frontend
]

# Add origins from environment variable if provided (comma-separated)
extra_origins_str = os.getenv("CORS_EXTRA_ORIGINS")
if extra_origins_str:
    extra_origins = [origin.strip() for origin in extra_origins_str.split(",")]
    ALLOWED_ORIGINS.extend(extra_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy", "version": "0.1.0"}


if __name__ == "__main__":
    import os

    import uvicorn

    # Get the port from environment variable, default to 8000 if not set
    port_str: str = os.environ.get("PORT", "8000")
    try:
        port: int = int(port_str)
    except ValueError:
        print(f"Invalid PORT value: '{port_str}'. Using default port 8000.")
        port = 8000

    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=False)


app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(task_routes.router, prefix="/api/v1/tasks", tags=["tasks"])
