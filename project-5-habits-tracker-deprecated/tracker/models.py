from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=50)  # e.g., daily, weekly, every X days
    start_date = models.DateField()
    time_of_day = models.TimeField()  # Changed to TimeField to store specific hours

    def __str__(self):
        return self.name

    def edit_habit(self, name=None, description=None, frequency=None, start_date=None, time_of_day=None):
        if name:
            self.name = name
        if description:
            self.description = description
        if frequency:
            self.frequency = frequency
        if start_date:
            self.start_date = start_date
        if time_of_day:
            self.time_of_day = time_of_day
        self.save()

    def delete_habit(self):
        self.delete()

class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='completions')
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.habit.name} completion on {self.date}: {'Completed' if self.completed else 'Not Completed'}"

    @classmethod
    def toggle_completion(cls, habit, date=None):
        date = date or timezone.now().date()
        completion, created = cls.objects.get_or_create(habit=habit, date=date)
        completion.completed = not completion.completed
        completion.save()
        return completion