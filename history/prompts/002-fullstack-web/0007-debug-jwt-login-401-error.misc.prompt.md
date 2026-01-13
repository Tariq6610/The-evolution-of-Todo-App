---
id: "0007"
title: "Debug JWT login 401 error"
stage: "misc"
date: "2026-01-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "002-fullstack-web"
branch: "phase-2-fullstack-web"
user: "User debugging JWT authentication 401 error"
command: "i am having 401 error using signIn although i am using right credentails, we are using jwt tokens check if we are using the same logic and decoding jwt access token in the right way"
labels: ["jwt", "authentication", "debug", "login"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "apps/002-fullstack-web/backend/src/adapters/api/auth_routes.py"
  - "apps/002-fullstack-web/backend/src/adapters/security/jwt.py"
  - "apps/002-fullstack-web/backend/src/domain/services/auth_service.py"
  - "apps/002-fullstack-web/backend/src/adapters/db/session.py"
  - "apps/002-fullstack-web/backend/.env"
tests: []
---

## Prompt

User reported 401 error during login despite using correct credentials. Investigation requested to check JWT token logic and decoding.

## Response snapshot

**Root Cause Identified:**

Multiple issues were found during debugging:

1. **Environment Variables Not Loading**: The `.env` file wasn't being loaded correctly because `load_dotenv()` was called without an absolute path. The backend was trying to connect to Neon PostgreSQL instead of local SQLite database.

2. **CORS Policy Error**: When using cookies (`withCredentials: true`), browsers require specific origins, not `*`. Fixed by changing `allow_origins=["*"]` to `allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]`.

3. **Dict vs Object Access Bug (THE MAIN ISSUE)**: In `auth_routes.py`, `create_token()` returns a dict `{"access_token": "..."}` but the code accessed it with `.access_token` (attribute access) instead of `["access_token"]` (dict key access).

**Debug Process:**
- Verified password verification works directly: `verify_password("12345678", hash)` returns `True`
- Added debug logging to trace authentication flow
- Discovered `authenticate()` succeeds but exception still raised
- Found error: `AttributeError: 'dict' object has no attribute 'access_token'`

**Fix Applied:**
```python
# Before (broken):
token_data = auth_service.create_token(user)
access_token = token_data.access_token  # AttributeError!

# After (fixed):
token_data = auth_service.create_token(user)
access_token = token_data["access_token"]  # Dict key access
```

## Outcome

- ✅ Impact: Fixed JWT login authentication. Login now returns successful response with access token.
- 🧪 Tests: Verified with curl: `curl -X POST "http://localhost:8000/api/v1/auth/login" -d "username=admin@gmail.com&password=12345678"` returns token.
- 📁 Files:
  - `apps/002-fullstack-web/backend/src/adapters/db/session.py` - Fixed `.env` loading with absolute path
  - `apps/002-fullstack-web/backend/src/main.py` - Fixed CORS origins for credentials
  - `apps/002-fullstack-web/backend/src/adapters/api/auth_routes.py` - Fixed dict access bug
  - `apps/002-fullstack-web/backend/.env` - Created with SQLite database URL
- 🔁 Next prompts: None required for this fix.
- 🧠 Reflection: Debug output was critical. The exception was caught by the try/except block which returned 401 with generic message. Adding `[DEBUG]` logging revealed the actual `AttributeError` that was being swallowed.

## Evaluation notes (flywheel)

- Failure modes observed:
  - Environment variables not loading due to relative path issues
  - CORS wildcard rejection when credentials are used
  - Generic exception handling masking real errors
- Graders run and results (PASS/FAIL): Manual verification PASS - login returns token.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add structured error logging to catch and log exceptions before re-raising.
