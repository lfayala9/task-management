from django.urls import path
from .views import index, tasks_view, delete_task, get_task, modify_task, task_api

urlpatterns = [
	path("", index, name="home"),
	path("tasks/", tasks_view, name="tasks"),
	path("tasks/<int:task_id>/delete/", delete_task, name="delete_task"),
	path("tasks/<int:task_id>/", get_task, name="task_detail"),
	path("tasks/<int:task_id>/update/", modify_task, name="modify_task"),
	path("api/tasks/<int:task_id>/", task_api, name="task_api"),
]