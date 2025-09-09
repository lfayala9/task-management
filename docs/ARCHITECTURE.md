# Architecture

## Overview
This project is a **Task Management System** built with **Django** and designed with a modular, containerized architecture.  
It combines a **REST API**, **asynchronous task processing**, and **secure authentication** while leveraging container orchestration with **Docker Compose**.

---

## Components

### 1. **Django Backend**
- Framework: **Django 4.2**
- Provides the REST API endpoints for:
  - User registration & authentication (**JWT-based**).
  - Task creation, listing, updating, and archival.
  - Notifications via Celery tasks.
- App structure:
  - `apps/users` → Custom user model (`User`) extending `AbstractUser`.
  - `apps/tasks` → Task model with metadata, due dates, priority, status, etc.
  - `apps/common` → Shared utilities.
  - `apps/tests` → Centralized test suite (pytest + pytest-django).

---

### 2. **Authentication**
- Authentication is handled with **JWT tokens**.
- Endpoints for:
  - `register` → user creation.
  - `login` → token issuance.
- Permissions:
  - Many endpoints (e.g., task list) require authentication → unauthorized users receive **401 Unauthorized**.

---

### 3. **Database**
- **PostgreSQL 17** runs as a dedicated service in Docker.
- Stores:
  - User accounts & roles.
  - Task data (title, description, due dates, priority, status, metadata).
  - Audit fields (`created_at`, `updated_at`).
- Managed via **Django ORM** and migrations.

---

### 4. **Caching & Queues**
- **Redis 8.2.1** serves dual purposes:
  - Caching layer.
  - **Message broker** for Celery workers.
- Requires authentication via Redis password (configured via `.env`).

---

### 5. **Asynchronous Processing**
- **Celery** handles background tasks, such as:
  - Sending email notifications when tasks are created or updated.
  - Future support for periodic cleanup jobs (via Celery Beat).
- Services:
  - `celery-worker`: executes async jobs.
  - `celery-beat`: schedules periodic tasks.

### 6 **Deployment Workflow**
1. Docker Compose orchestrates services:
   - `db` and `cache` boot first.
   - `django` waits for database before running migrations.
   - Celery workers connect to Redis and listen for jobs.
2. Entry point script (`scripts/entrypoint.sh`) manages initialization.
3. Developers interact with API via `http://localhost:8000`.

Example Celery task:
```python
@shared_task
def send_task_notification(task_id, notification_type):
    task = Task.objects.get(id=task_id)
    recipients = [task.created_by.email]
    subject = f"Task {task_id} - {notification_type}"
    message = f"Task {task_id} has been {notification_type}."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients)
    return f"Email sent for task {task_id}"


           ┌───────────────┐
           │   Frontend    │
           │  (REST API)   │
           └───────▲───────┘
                   │
                   ▼
         ┌───────────────────┐
         │   Django (API)    │
         │   JWT Auth, ORM   │
         └───────┬───────────┘
                 │
 ┌───────────────┼───────────────┐
 │               │               │
 ▼               ▼               ▼
PostgreSQL     Redis        Celery Worker
 (DB)     (Cache/Broker)   (Async Jobs)
                 │
                 ▼
           Celery Beat
         (Scheduled Tasks)