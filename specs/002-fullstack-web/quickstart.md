# Quickstart Guide: Phase II - Full-Stack Web Application

## Development Environment Setup

### 1. Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configure your NEON_DB_URL
```

### 2. Frontend (Next.js)
```bash
cd frontend
npm install
cp .env.example .env.local  # Configure NEXT_PUBLIC_API_URL
```

## Running the Application

### Start Backend
```bash
cd backend
activate-venv
uvicorn src.adapters.api.main:app --reload
```

### Start Frontend
```bash
cd frontend
npm run dev
```

## Database Migrations
We use Alembic for database migrations with SQLModel.
```bash
cd backend
alembic revision --autogenerate -m "Init Phase II schema"
alembic upgrade head
```

## Testing Workflow

### Backend (BDD + Unit)
```bash
cd backend
pytest
```

### Frontend (E2E)
```bash
cd frontend
npx playwright test
```

## Hexagonal Architecture Rules

1. **Domain Logic Only**: No FastAPI or SQLModel dependencies in `src/domain`.
2. **Ports as Protocols**: Define repository behaviors as Python Protocols in `src/ports`.
3. **Dependency Injection**: Use FastAPI `Depends` to inject Adapters into the Domain Services.
4. **Data Isolation**: Always pass `current_user.id` to repository methods to ensure multi-user isolation.
