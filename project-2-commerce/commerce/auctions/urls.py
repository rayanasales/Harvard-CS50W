from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create/', views.create_listing, name='create_listing'),
    path("listing/<int:listing_id>", views.listing_details, name="listing_details"),
    path("listing/<int:listing_id>/toggle_watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/post_comment", views.post_comment, name="post_comment"),  # New URL for posting comments
]