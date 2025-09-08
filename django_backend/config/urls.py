from django.urls import path
from .views import index, tasks_view, delete_task, find_task, task_api, task_list_api, register, login, create_tag

urlpatterns = [
	path("", index, name="home"),
	path("tasks/", tasks_view, name="tasks"),
	path("tasks/<int:task_id>/", find_task, name="task_detail"),
	path("tasks/<int:task_id>/delete/", delete_task, name="delete_task"),
	path("api/tasks/", task_list_api, name="task_list_api"),
	path("api/tasks/<int:task_id>/", task_api, name="task_api"),
	path("register/", register, name="register"),
	path("login/", login, name="login"),
	path("tags/create/", create_tag, name="create_tag"),
]