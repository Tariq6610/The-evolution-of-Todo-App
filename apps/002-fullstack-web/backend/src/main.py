import os
from collections.abc import Awaitable, Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.adapters.api import auth_routes, task_routes
from src.adapters.db.session import init_db


class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle proxy headers from Railway and other reverse proxies.
    Ensures that HTTPS protocol is preserved in redirects and URL generation.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Check for forwarded headers from Railway proxy
        forwarded_proto = request.headers.get("x-forwarded-proto", "")
        if forwarded_proto.lower() == "https":
            # Update the request's URL scheme to reflect HTTPS
            request.scope["scheme"] = "https"

        response = await call_next(request)
        return response


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
    "https://frontend-orpin-seven-86.vercel.app",  # Vercel frontend
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
    allow_headers=[
        "Access-Control-Allow-Origin",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "X-CSRFToken",
    ],
    # Expose the headers that frontend can access
    expose_headers=[
        "Access-Control-Allow-Origin",
        "Content-Type",
        "Authorization",
        "Set-Cookie",
    ],
)

# Add proxy headers middleware to handle HTTPS redirects properly behind Railway proxy
app.add_middleware(ProxyHeadersMiddleware)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "Backend is running"}


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
