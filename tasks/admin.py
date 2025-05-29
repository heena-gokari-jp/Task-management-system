from django.contrib import admin
from .models import Task, Category

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Task model.
    - Displays title, priority, status, due date, and associated user.
    - Adds filtering by status, priority, and categories.
    - Enables search by title and description.
    """
    list_display = ('title', 'priority', 'status', 'due_date', 'user')
    list_filter = ('status', 'priority', 'categories')
    search_fields = ('title', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Category model.
    - Displays category name and associated user.
    - Enables search by name.
    """
    list_display = ('name', 'user')
    search_fields = ('name',)
