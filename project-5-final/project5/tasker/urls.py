
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/create/", views.create_task, name="create_task"),
    path("tasks/edit/<int:task_id>/", views.edit_task, name="edit_task"),
    path("tasks/update_status/<int:task_id>/<str:new_status>/", views.update_task_status, name="update_task_status"),
    path("tasks/delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path("tasks/duplicate/<int:task_id>/", views.duplicate_task, name="duplicate_task"),
    path("tasks/add_tag/", views.add_tag, name="add_tag"),
    path("tags/", views.tag_list, name="tag_list"),
    path("tags/create/", views.create_tag, name="create_tag"),
    path("tags/delete/<int:tag_id>/", views.delete_tag, name="delete_tag"),
]
