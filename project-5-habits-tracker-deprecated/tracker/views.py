from django.shortcuts import render
from .models import Habit, HabitCompletion
from datetime import datetime, timedelta

def index(request):
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
    habits = Habit.objects.filter(start_date__lte=end_of_week)

    context = {
        'habits': habits,
        'week_dates': week_dates,
    }
    return render(request, 'tracker/index.html', context)