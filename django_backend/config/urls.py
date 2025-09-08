from django.urls import path
from .views import index, auth_api, tasks_view, delete_task, find_task, task_api, task_list_api, register, login_user, create_tag, create_comment, user_api

urlpatterns = [
	path("", index, name="home"),
	path("tasks/", tasks_view, name="tasks"),
	path("tasks/<int:task_id>/", find_task, name="task_detail"),
	path("tasks/<int:task_id>/delete/", delete_task, name="delete_task"),
	path("register/", register, name="register"),
	path("login/", login_user, name="login"),
	path("tags/create/", create_tag, name="create_tag"),
	path("tasks/<int:task_id>/comments/create/", create_comment, name="create_comment"),
	path("api/tasks/", task_list_api, name="task_list_api"),
	path("api/tasks/<int:task_id>/", task_api, name="task_api"),
	path("api/auth/<str:action>/", auth_api, name="auth_api"),
	path("api/users/<int:user_id>/", user_api, name="user_api"),
	path("api/users/", user_api, name="user_api"),
]