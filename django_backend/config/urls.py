from django.urls import path
from .views import index, tasks_view

urlpatterns = [
	path("", index, name="home"),
	path("tasks/", tasks_view, name="tasks"),
]