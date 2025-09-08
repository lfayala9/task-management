from django.db import models
from apps.users.models import User

STATUS_CHOICES = [
	("pending", "Pending"),
	("in_progress", "In Progress"),
	("completed", "Completed"),
	("on_hold", "On Hold"),
	("cancelled", "Cancelled"),
]

PRIORITY_CHOICES = [
	("low", "Low"),
	("medium", "Medium"),
	("high", "High"),
	("urgent", "Urgent"),
]

class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __str__(self):
		return self.name

class Comment(models.Model):
	task = models.ForeignKey("Task", related_name="comments", on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

class TaskAssignment(models.Model):
	task = models.ForeignKey("Task", on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	assigned_at = models.DateTimeField(auto_now_add=True)
	role = models.CharField(max_length=100, blank=True, default="")
	class Meta:
		unique_together = ("task", "user")
	def __str__(self):
		return f"{self.user.username} assigned to {self.task.title}"

class TaskHistory(models.Model):
	task = models.ForeignKey("Task", related_name="history", on_delete=models.CASCADE)
	changed_at = models.DateTimeField(auto_now_add=True)
	changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	old_value = models.TextField(null=True, blank=True)
	new_value = models.TextField(null=True, blank=True)
	field_changed = models.CharField(max_length=100)

	def __str__(self):
		return f"Change on {self.task.title} at {self.changed_at}"

class Task(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	status = models.CharField(choices=STATUS_CHOICES, null=True)
	priority = models.CharField(choices=PRIORITY_CHOICES, default="medium")
	due_date = models.DateField(default=None)
	estimated_hours = models.DecimalField(null=True, blank=True, default=None, max_digits=5, decimal_places=2)
	actual_hours = models.DecimalField(null=True, blank=True, default=None, max_digits=5, decimal_places=2)

	created_by = models.ForeignKey(User, related_name="tasks_created", on_delete=models.CASCADE, default=1)
	assigned_to = models.ManyToManyField(User, related_name="tasks_assigned", through=TaskAssignment)
	tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")
	parent_task = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

	metadata = models.JSONField(default=dict)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_archived = models.BooleanField(default=False)
