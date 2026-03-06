#!/bin/bash

echo "Testing Backend API Endpoints..."

# Test health endpoint
echo "Testing health endpoint..."
curl -X GET http://localhost:8000/health
echo -e "\n"

# Test auth endpoints - first try to register a user
echo "Testing registration endpoint..."
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User"
  }'
echo -e "\n"

# Test login with the registered user
echo "Testing login endpoint..."
LOGIN_RESPONSE=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=test@example.com&password=testpassword123' \
  -s)

echo "Login response: $LOGIN_RESPONSE"
echo -e "\n"

# Extract token from response (simplified - in real scenario you'd parse JSON properly)
TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "Extracted token: $TOKEN"
echo -e "\n"

if [ ! -z "$TOKEN" ]; then
  echo "Testing task endpoints with authentication..."

  # Test creating a task
  echo "Creating a task..."
  curl -X POST http://localhost:8000/api/v1/tasks/ \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "title": "Test Task",
      "description": "This is a test task",
      "priority": "MEDIUM"
    }'
  echo -e "\n"

  # Test getting all tasks
  echo "Getting all tasks..."
  curl -X GET http://localhost:8000/api/v1/tasks/ \
    -H "Authorization: Bearer $TOKEN"
  echo -e "\n"
else
  echo "No token received, skipping authenticated requests"
fi

echo "API verification completed!"