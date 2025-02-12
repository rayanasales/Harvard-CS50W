from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^wiki/(?P<title>[\w-]+)/?$', views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create", views.create_new_page, name="create_new_page"),
    path("edit/<str:title>", views.edit_page, name="edit_page"),
    path("random", views.random_page, name="random_page"),
]

# The issue might be related to how Django handles URLs with trailing slashes. 
# By default, Django's APPEND_SLASH setting is enabled, which automatically 
# redirects URLs without a trailing slash to URLs with a trailing slash if no match is found.

# To fix this issue, you can explicitly handle the trailing slash in your URL patterns. 
# You can use a regular expression to match both URLs with and without a trailing slash.

# By using re_path with a regular expression, you can match both wiki/Git and wiki/Git/ URLs.
# Additionally, ensure that APPEND_SLASH is set to False in your settings.py to prevent automatic redirection:
# APPEND_SLASH = False
