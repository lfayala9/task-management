# API Documentation

## Overview
This document describes the REST API endpoints of the **Task Management System**.  
The API uses **JWT-based authentication** and exposes endpoints for **user management** and **task management**.  

All responses are in **JSON** format.  

---

## Authentication
- Authentication is handled via **JWT tokens**.
- After logging in, clients must include the token in the `Authorization` header:

## User Endpoints

### 1. Register a New User
**POST** `/api/users/register/`

**Request:**
```json
{
  "username": "john",
  "password": "12345",
  "email": "john@example.com"
}
```
**Response 200:**

```json
{
  "username": "john",
  "email": "john@example.com"
}
```
### 2. Login and logout a User

**POST** `/api/users/login/`

**Request:**
```json
{
  "username": "john",
  "password": "12345",
  "email": "john@example.com"
}
```

**POST** `/api/users/logout/`

**Request:**

**Response 200:**

```json
{
  "refresh": "<JWT_REFRESH_TOKEN>"
}
```
### 3. Refresh

**POST** `/api/users/refresh/`

```json
{
  "refresh": "<JWT_REFRESH_TOKEN>"
}
```

**Response 200:**

```json
{
  "access": "<JWT_ACCESS_TOKEN>",
}
```

## Task Endpoints

### 1. Get tasks

**GET** `/api/tasks/`

**Response 200:**
```json
[
  {
    "id": 1,
    "title": "Integration Test",
    "description": "Test Celery",
    "status": "pending",
    "due_date": "2025-09-10",
    "created_by": 1
  }
]
```

## If user not authenticated
```json

{
  "detail": "Authentication credentials were not provided."
}
```

### 2. Create a task

**POST** `/api/tasks/`

**Request:**
```json
{
  "title": "Write API docs",
  "description": "Document all endpoints",
  "due_date": "2025-09-15"
}
```

**Response: 201**
```json
{
  "id": 2,
  "title": "Write API docs",
  "description": "Document all endpoints",
  "status": "pending",
  "due_date": "2025-09-15",
  "created_by": 1
}
```

### 3. Get a single task

**GET** `/api/tasks/<id>`

## Need to be authenticated 

**Response: 201**
```json
{
  "id": 2,
  "title": "Write API docs",
  "description": "Document all endpoints",
  "status": "pending",
  "due_date": "2025-09-15",
  "created_by": 1
}
```
### 4. Update a task

**PUT** `/api/tasks/<id>`

**Request:**
```json
{
  "title": "Write API docs",
  "description": "Updated description",
  "status": "in_progress",
  "due_date": "2025-09-20"
}
```

**Response: 200**
```json
{
  "id": 2,
  "title": "Write API docs",
  "description": "Updated description",
  "status": "in_progress",
  "due_date": "2025-09-20",
  "created_by": 1
}
```

### 5. Delete a task

**DELETE** `/api/tasks/<id>`

## Requires authentication

**Response: 204** 

(no body)


### Tests

## Endpoint testing with curl

# 1. Register user
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "12345", "email": "john@example.com"}'

# 2. Login and capture token
TOKEN=$(curl -s -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "password": "12345"}' | jq -r .access)

# 3. Create a task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "First Task", "description": "Test task creation", "due_date": "2025-09-15"}'

# 4. List tasks
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer $TOKEN"