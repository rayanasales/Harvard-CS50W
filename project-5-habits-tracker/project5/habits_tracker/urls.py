
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_habit", views.create_habit, name="create_habit"),
    path("toggle_completion/<int:habit_id>/<str:date>/", views.toggle_completion, name="toggle_completion"),
]
