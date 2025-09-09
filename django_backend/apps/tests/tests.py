import pytest
from apps.tasks.models import Task
from apps.users.models import User
from rest_framework.test import APIClient
from apps.tasks.celery_tasks import send_task_notification
from datetime import date
from django.urls import reverse

@pytest.mark.django_db
def test_create_task():
    user = User.objects.create_user(username="testuser", password="123")
    task = Task.objects.create(
        title="Test Task",
        description="Testing model",
        created_by=user,
        status="todo",
        due_date=date.today()
    )
    assert task.title == "Test Task"
    assert task.created_by.username == "testuser"

@pytest.mark.django_db
def test_task_list_requires_auth():
    client = APIClient()
    url = reverse("task_list_api")
    response = client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_register_and_login():
    client = APIClient()
    response = client.post(
        reverse("auth_api", args=["register"]),
        {"username": "newuser", "password": "123", "email": "test@test.com"},
        format="json"
    )
    assert response.status_code == 200
    response = client.post(
        reverse("auth_api", args=["login"]),
        {"username": "newuser", "password": "123"},
        format="json"
    )
    assert response.status_code == 200
    assert "user_id" in response.json()

@pytest.mark.django_db
def test_celery_task_notification():
    user = User.objects.create_user(username="john", password="123", email="john@test.com")
    task = Task.objects.create(title="Integration Test", description="Test Celery", created_by=user, due_date=date.today())
    result = send_task_notification.delay(task.id, "created")
    output = result.get(timeout=10)
    assert output.startswith("Email sent for task")