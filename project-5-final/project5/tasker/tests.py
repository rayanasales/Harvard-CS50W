from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Task
from datetime import date

User = get_user_model()

class TaskManagerTests(TestCase):
    
    def setUp(self):
        """Set up a test user and test tasks."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        self.task1 = Task.objects.create(
            user=self.user,
            name="Test Task 1",
            description="This is the first test task.",
            date_to_complete=date.today(),
            size="medium",
            priority="urgent",
            status="in-analysis"
        )

        self.task2 = Task.objects.create(
            user=self.user,
            name="Test Task 2",
            description="This is the second test task.",
            date_to_complete=date.today(),
            size="small",
            priority="light",
            status="completed"
        )

    def test_index_redirects_to_task_list(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasker/task_list.html")

    def test_login_view(self):
        response = self.client.post(reverse("login"), {"username": "testuser", "password": "password123"})
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_logout_view(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

    def test_register_view(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "confirmation": "newpassword"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_task_list_view(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasker/task_list.html")
        self.assertContains(response, "Test Task 1")
        self.assertContains(response, "Test Task 2")

    def test_create_task_view(self):
        response = self.client.post(reverse("create_task"), {
            "name": "New Task",
            "description": "Newly created task.",
            "date_to_complete": date.today(),
            "size": "large",
            "priority": "medium",
            "status": "in-progress"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_edit_task_view(self):
        response = self.client.post(reverse("edit_task", args=[self.task1.id]), {
            "name": "Updated Task",
            "description": "Updated description.",
            "date_to_complete": date.today(),
            "size": "extraLarge",
            "priority": "severe",
            "status": "flagged"
        })
        self.assertEqual(response.status_code, 302)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, "Updated Task")
        self.assertEqual(self.task1.status, "flagged")

    def test_update_task_status_view(self):
        response = self.client.post(reverse("update_task_status", args=[self.task1.id, "completed"]))
        self.assertEqual(response.status_code, 200)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, "completed")

    def test_delete_task_view(self):
        response = self.client.post(reverse("delete_task", args=[self.task1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())