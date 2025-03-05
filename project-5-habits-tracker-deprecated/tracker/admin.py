from django.contrib import admin
from .models import Habit, HabitCompletion

class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'start_date', 'time_of_day')
    search_fields = ('name', 'description')
    list_filter = ('start_date', 'user')
    actions = ['delete_selected']

class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'completed')
    list_filter = ('completed', 'date')
    search_fields = ('habit__name',)
    actions = ['toggle_completion']

    def toggle_completion(self, request, queryset):
        for completion in queryset:
            completion.completed = not completion.completed
            completion.save()
    toggle_completion.short_description = "Toggle selected completions"

admin.site.register(Habit, HabitAdmin)
admin.site.register(HabitCompletion, HabitCompletionAdmin)