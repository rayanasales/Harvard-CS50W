
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("like/<int:post_id>", views.like_toggle, name="like_toggle"),
    path("edit/<int:post_id>", views.edit_post, name="edit_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/follow", views.toggle_follow, name="toggle_follow"),
    path("following", views.following_posts, name="following"),
]
