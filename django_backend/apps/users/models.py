from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	role = models.CharField(max_length=50, blank=True, null=True)
	metadata = models.JSONField(default=dict)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)