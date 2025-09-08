from apps.tasks.models import Tag, Task
from apps.users.models import User
from datetime import date
from decimal import Decimal

user, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@example.com"})
user.set_password("admin123")
user.save()

default_tags = ["bug", "feature", "improvement", "documentation", "backend", "frontend"]
for t in default_tags:
    Tag.objects.get_or_create(name=t)

if not Task.objects.exists():
    task1 = Task.objects.create(
        title="Fix login bug",
        description="Users cannot log in under certain conditions.",
        status="in_progress",
        priority="high",
        due_date=date.today(),
        estimated_hours=Decimal("2.5"),
        actual_hours=Decimal("1.0"),
        created_by=user
    )
    task2 = Task.objects.create(
        title="Add new feature",
        description="Implement the new dashboard feature.",
        status="pending",
        priority="medium",
        due_date=date.today(),
        estimated_hours=Decimal("5.0"),
        actual_hours=Decimal("0.0"),
        created_by=user
    )

    task1.tags.set(Tag.objects.filter(name__in=["bug", "backend"]))
    task2.tags.set(Tag.objects.filter(name__in=["feature", "frontend"]))
    task1.assigned_to.set([user])
    task2.assigned_to.set([user])

