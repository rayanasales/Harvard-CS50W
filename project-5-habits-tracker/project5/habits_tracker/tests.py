from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, time
from .models import Habit, HabitCompletion, HabitList

User = get_user_model()

class HabitTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

        self.habit1 = Habit.objects.create(user=self.user, name="Morning Run", frequency="daily", start_date=timezone.now().date(), hour=time(6, 0))
        self.habit2 = Habit.objects.create(user=self.user, name="Read a Book", frequency="daily", start_date=timezone.now().date(), hour=time(8, 0))
        self.habit3 = Habit.objects.create(user=self.user, name="Drink Water", frequency="daily", start_date=timezone.now().date(), hour=time(10, 0))
        self.habit4 = Habit.objects.create(user=self.user, name="Stretch", frequency="daily", start_date=timezone.now().date(), hour=time(14, 0))
        self.habit5 = Habit.objects.create(user=self.user, name="Journal", frequency="daily", start_date=timezone.now().date(), hour=time(22, 0))

        self.habit_list = HabitList.objects.create(user=self.user)
        self.habit_list.habits.add(self.habit1, self.habit2, self.habit3, self.habit4, self.habit5)

    def test_habit_list_contains_habits(self):
        self.assertEqual(self.habit_list.habits.count(), 5)
        self.assertIn(self.habit1, self.habit_list.habits.all())

    def test_create_habit(self):
        habit_count_before = Habit.objects.count()
        new_habit = Habit.objects.create(user=self.user, name="New Habit", frequency="weekly", start_date=timezone.now().date(), hour=time(12, 0))
        self.habit_list.habits.add(new_habit)
        habit_count_after = Habit.objects.count()
        self.assertEqual(habit_count_after, habit_count_before + 1)
        self.assertIn(new_habit, self.habit_list.habits.all())

    def test_edit_habit(self):
        self.habit1.name = "Updated Habit Name"
        self.habit1.save()
        updated_habit = Habit.objects.get(id=self.habit1.id)
        self.assertEqual(updated_habit.name, "Updated Habit Name")

    def test_remove_habit(self):
        self.habit_list.habits.remove(self.habit1)
        self.habit1.delete()
        self.assertEqual(self.habit_list.habits.count(), 4)

    def test_list_habits_per_day(self):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
        active_habits = Habit.objects.filter(start_date__lte=week_dates[-1])

        self.assertTrue(self.habit1 in active_habits)
        self.assertTrue(self.habit2 in active_habits)

    def test_mark_habit_as_completed(self):
        today = timezone.now().date()
        completion = HabitCompletion.objects.create(user=self.user, habit=self.habit1, date=today, completed=True)
        self.assertTrue(completion.completed)
        self.assertEqual(completion.habit, self.habit1)

    def test_mark_habit_as_incomplete(self):
        today = timezone.now().date()
        completion = HabitCompletion.objects.create(user=self.user, habit=self.habit1, date=today, completed=True)
        completion.completed = False
        completion.save()
        updated_completion = HabitCompletion.objects.get(id=completion.id)
        self.assertFalse(updated_completion.completed)