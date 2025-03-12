from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Task, Tag
from .forms import TaskForm
import json
from .models import User


def index(request):
    return task_list(request)


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
            return render(request, "tasker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "tasker/login.html")


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
            return render(request, "tasker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "tasker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tasker/register.html")


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    task_status = {
        "in_analysis": tasks.filter(status="in-analysis"),
        "in_progress": tasks.filter(status="in-progress"),
        "flagged": tasks.filter(status="flagged"),
        "completed": tasks.filter(status="completed"),
    }

    return render(request, "tasker/task_list.html", {"task_status": task_status})


@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()  # Save ManyToMany relationships
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasker/create_task.html", {"form": form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasker/edit_task.html", {"form": form, "task": task})


@csrf_exempt
@login_required
def update_task_status(request, task_id, new_status):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.status = new_status
    task.save()
    return JsonResponse({"message": "Task status updated successfully."})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return JsonResponse({"message": "Task deleted successfully."})


@login_required
def duplicate_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    duplicated_task = Task.objects.create(
        user=request.user,
        name=f"{task.name} (Copy)",
        description=task.description,
        date_to_complete=task.date_to_complete,
        size=task.size,
        priority=task.priority,
        status=task.status,
    )
    return JsonResponse({"message": "Task duplicated successfully."})


@login_required
def add_tag(request):
    if request.method == "POST":
        data = json.loads(request.body)
        tag_name = data.get("name")
        tag_color = data.get("color", "#000000")

        if not tag_name:
            return JsonResponse({"error": "Tag name is required"}, status=400)

        tag, created = Tag.objects.get_or_create(name=tag_name, defaults={"color": tag_color})
        return JsonResponse({"success": True, "tag_id": tag.id})