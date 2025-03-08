
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/create/", views.create_task, name="create_task"),
]
