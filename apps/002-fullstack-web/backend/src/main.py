from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.adapters.db.session import init_db

app = FastAPI(
    title="Todo Evolution API",
    description="Full-stack Todo application backend for Phase II",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "0.1.0"}

# Import and include routers here as they are implemented
from src.adapters.api import auth_routes, task_routes
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(task_routes.router, prefix="/api/v1/tasks", tags=["tasks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
