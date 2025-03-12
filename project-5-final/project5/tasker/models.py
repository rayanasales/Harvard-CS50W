from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default="#000000")  # Hex Color

    def __str__(self):
        return self.name


class Task(models.Model):
    SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('extraLarge', 'Extra Large'),
    ]

    PRIORITY_CHOICES = [
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('urgent', 'Urgent'),
        ('severe', 'Severe'),
    ]

    STATUS_CHOICES = [
        ('in-analysis', 'In Analysis'),
        ('in-progress', 'In Progress'),
        ('flagged', 'Flagged'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_to_complete = models.DateField()
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in-analysis')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"