from django.db import models

class Task(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	# status = models.CharField(choices=STATUS_CHOICES)
	# priority = models.CharField(choices=PRIORITY_CHOICES)
	# due_date = models.DateField()
	# estimated_hours = models.DecimalField(null=True, blank=True, default=None, max_digits=5, decimal_places=2)
	# actual_hours = models.DecimalField(null=True, blank=True, default=None, max_digits=5, decimal_places=2)

	# created_by = models.ForeignKey(User)
	# assigned_to = models.ManyToManyField(User)
	# tags = models.ManyToManyField(Tag)
	# parent_task = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

	# metadata = models.JSONField(default=dict)
	# created_at = models.DateTimeField(auto_now_add=True)
	# updated_at = models.DateTimeField(auto_now=True)
	# is_archived = models.BooleanField(default=False)