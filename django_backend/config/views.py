import json
from django.http import JsonResponse
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
	tasks = Task.objects.all()
	return render(request, "tasks.html", {"tasks": tasks})

def delete_task(request, task_id):
	try:
		task = Task.objects.get(id=task_id)
		task.delete()
	except Task.DoesNotExist:
		logger.error(f"Task with id {task_id} does not exist.")
	return redirect("/tasks/")

def get_task(request, task_id):
	try:
		task = Task.objects.get(id=task_id)
	except Task.DoesNotExist:
		logger.error(f"Task with id {task_id} does not exist.")
		return redirect("/tasks/")
	return render(request, "task_detail.html", {"task": task})

def modify_task(request, task_id):
	try:
		task = Task.objects.get(id=task_id)
	except Task.DoesNotExist:
		logger.error(f"Task with id {task_id} does not exist.")
		return redirect("/tasks/")
	task.title = request.POST.get("title", task.title)
	task.description = request.POST.get("description", task.description)
	task.save()
	return redirect(f"/tasks/{task.id}/")

def task_list_api(request):
	if request.method == "GET":
		tasks = Task.objects.all()
		tasks_data = [{
			"id": task.id,
			"title": task.title,
			"description": task.description,
			"metadata": task.metadata,
			"created_at": task.created_at,
			"updated_at": task.updated_at,
			"is_archived": task.is_archived
		} for task in tasks]
		return JsonResponse(tasks_data, safe=False)
	elif request.method == "POST":
		data = json.loads(request.body)
		task = Task(
			title=data.get("title"),
			description=data.get("description"),
			metadata=data.get("metadata", {})
		)
		task.save()
		return JsonResponse({"id": task.id}, status=201)
	return JsonResponse({"error": "Method not allowed"}, status=405)

def task_api(request, task_id):
	try:
		task = Task.objects.get(id=task_id)
		if request.method == "GET":
			return JsonResponse({
				"id": task.id,
				"title": task.title,
				"description": task.description,
				"metadata": task.metadata,
				"created_at": task.created_at,
				"updated_at": task.updated_at,
				"is_archived": task.is_archived
			})
		elif request.method == "PUT":
			data = json.loads(request.body)
			task.title = data.get("title", task.title)
			task.description = data.get("description", task.description)
			task.metadata = data.get("metadata", task.metadata)
			task.is_archived = data.get("is_archived", task.is_archived)
			task.save()
			return JsonResponse({"status": "success"})
		elif request.method == "PATCH":
			data = json.loads(request.body)
			if "title" in data:
				task.title = data["title"]
			if "description" in data:
				task.description = data["description"]
			if "metadata" in data:
				task.metadata = data["metadata"]
			if "is_archived" in data:
				task.is_archived = data["is_archived"]
			task.save()
			return JsonResponse({"status": "success"})
		elif request.method == "DELETE":
			task.delete()
			return JsonResponse({"status": "deleted"})
	except Task.DoesNotExist:
		logger.error(f"Task with id {task_id} does not exist.")
		return JsonResponse({"error": "Task not found"}, status=404)
	return JsonResponse({"error": "Method not allowed"}, status=405)