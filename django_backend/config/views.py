from django.shortcuts import render, redirect
import logging
from apps.tasks.models import Task

logger = logging.getLogger(__name__)
def index(request):
	return render(request, "index.html")

def tasks_view(request):
	if request.method == "POST":
		logger.info(f"Complete QueryDict: {request.POST}")
		task = Task(title=request.POST.get("title"), description=request.POST.get("description"))
		task.save()
		return redirect("/tasks/")
	return render(request, "tasks.html")