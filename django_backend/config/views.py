from apps.tasks.models import Task, Tag
from apps.users.models import User
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import logging
import json

logger = logging.getLogger(__name__)

def index(request):
	return render(request, "index.html")

def register(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		email = request.POST.get("email", "")
		if not username or not password:
			return render(request, "register.html", {"error": "Username and password are required."})
		if User.objects.filter(username=username).exists():
			return render(request, "register.html", {"error": "Username already exists."})
		user = User.objects.create_user(username=username, password=password, email=email)
		user.save()
		return redirect("/")
	return render(request, "register.html")

def login(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = User.objects.filter(username=username).first()
		if user and user.check_password(password):
			request.session['user_id'] = user.id
			return redirect("/tasks/")
		else:
			return render(request, "login.html", {"error": "Invalid username or password."})
	return render(request, "index.html")

def get_task(id, ret_val):
	try:
		task = Task.objects.get(id=id)
	except Task.DoesNotExist:
		logger.error(f"Task with id {id} does not exist.")
		return ret_val
	return task

def do_task(task):
	data = model_to_dict(task)
	data["created_by"] = task.created_by.id if task.created_by else None
	data["assigned_to"] = task.assigned_to.id if task.assigned_to else None
	data["tags"] = [tag.id for tag in task.tags.all()]
	data["parent_task"] = task.parent_task.id if task.parent_task else None
	return data

def tasks_view(request):
	if request.method == "POST":
		created_by_id = request.POST.get("created_by")
		parent_task_id = request.POST.get("parent_task")
		parent_task = Task.objects.filter(id=parent_task_id).first() if parent_task_id else None
		created_by = None
		if created_by_id:
			try:
				created_by = User.objects.get(id=created_by_id)
			except User.DoesNotExist:
				pass	
		logger.info(f"Complete QueryDict: {request.POST}")
		data = {
			"title": request.POST["title"],
			"description": request.POST["description"],
			"status": request.POST["status"],
			"priority": request.POST["priority"],
			"due_date": request.POST["due_date"],
			# "tags": request.POST.getlist("tags"),
			"estimated_hours": request.POST["estimated_hours"],
			"actual_hours": request.POST["actual_hours"],
			"created_by": created_by,
			"parent_task": parent_task,
			"metadata": json.loads(request.POST.get("metadata", "{}")),
		}
		task = Task.objects.create(**data)
		assigned_to = request.POST.getlist("assigned_to")
		if assigned_to:
			task.assigned_to.set(assigned_to)
		tags = request.POST.getlist("tags")
		if tags:
			tag_objs = Tag.objects.filter(name__in=tags)
			task.tags.set(tag_objs)
		task.save()
		return redirect("/tasks/")
	tasks = Task.objects.all()
	tags = Tag.objects.all()
	return render(request, "tasks.html", {"tasks": tasks, "tags": tags})

def delete_task(request, task_id):
	task = get_task(task_id, JsonResponse({"error": "Task not found"}, status=404))
	if task:
		task.delete()
	return redirect("/tasks/")

def find_task(request, task_id):
	task = get_object_or_404(Task, pk=task_id)
	task_tag_names = list(task.tags.values_list('name', flat=True))
	if request.method == "POST":
		task.title = request.POST.get("title", task.title)
		task.description = request.POST.get("description", task.description)
		task.save()
		tag_names = request.POST.getlist("tags")
		if tag_names:
			tag_objs = Tag.objects.filter(name__in=tag_names)
			task.tags.set(tag_objs)
		return redirect(f"/tasks/{task.id}/")
	return render(request, "task_detail.html", {"task": task, "task_tag_names": task_tag_names})

@csrf_exempt
def task_list_api(request):
	if request.method == "GET":
		tasks = Task.objects.all()
		task_list = [do_task(task) for task in tasks]
		return JsonResponse(task_list, safe=False)
	return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def  task_api(request, task_id):
	task = get_task(task_id, JsonResponse({"error": "Task not found"}, status=404))
	if not task:
		return JsonResponse({"error": "Task not found"}, status=404)
	if request.method == "GET":
		return JsonResponse(do_task(task))
	elif request.method in ["PUT", "PATCH"]:
		try:
			data = json.loads(request.body)
			for field in ["title", "description", "status", "tags" ,"priority", "due_date",
						  "estimated_hours", "actual_hours", "metadata", "is_archived"]:
				if field in data:
					setattr(task, field, data[field])
			if "created_by" in data:
				task.created_by_id = data["created_by"]
			if "parent_task" in data:
				task.parent_task_id = data["parent_task"]
			if "assigned_to" in data:
				task.assigned_to.set(data["assigned_to"])
			if "tags" in data:
				task.tags.set(data["tags"])
			task.save()
			return JsonResponse({"status": "success"})
		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON"}, status=400)
		except Exception as e:
			logger.error(f"Error updating task: {e}")
			return JsonResponse({"error": "Internal server error"}, status=500)
	elif request.method == "DELETE":
		task.delete()
		return JsonResponse({"status": "deleted"})
	return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def create_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Tag.objects.create(name=name)
        return redirect('tasks')
    return render(request, 'create_tag.html')