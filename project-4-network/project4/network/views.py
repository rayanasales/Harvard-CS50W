from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

import json

from .models import User, Post


def index(request):
    post_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(post_list, 10)  # Show 10 posts per page.

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "network/index.html", {'page': page})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        post = Post(user=request.user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/new_post.html") 


@login_required
def follow_toggle(request, username):
    target_user = User.objects.get(username=username)
    if target_user in request.user.following.all():
        request.user.following.remove(target_user)
    else:
        request.user.following.add(target_user)
    return HttpResponseRedirect(reverse("index"))


@login_required
def like_toggle(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return JsonResponse({'liked': request.user in post.likes.all(), 'like_count': post.likes.count()})


@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user != post.user:
        return JsonResponse({'error': 'You do not have permission to edit this post'}, status=403)
    if request.method == 'POST':
        data = json.loads(request.body)
        post.content = data['content']
        post.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all().order_by('-timestamp')
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    is_following = request.user in profile_user.followers.all()

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    })


@login_required
def toggle_follow(request, username):
    profile_user = get_object_or_404(User, username=username)
    if profile_user != request.user:
        if request.user in profile_user.followers.all():
            profile_user.followers.remove(request.user)
        else:
            profile_user.followers.add(request.user)

    return HttpResponseRedirect(reverse('profile', args=[username]))