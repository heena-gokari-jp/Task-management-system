from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Model representing a task category.

    Each category is associated with a specific user. Categories are used to group and
    organize tasks. A user cannot have two categories with the same name.

    Fields:
        name (str): Name of the category.
        user (ForeignKey): The user who owns the category.
    """

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['name', 'user']


class Task(models.Model):
    """
    Model representing a task in the task management system.

    Tasks have priorities, statuses, optional due dates, and can be associated with
    multiple categories. Each task is linked to the user who created it.

    Fields:
        title (str): Title of the task.
        description (str): Optional description of the task.
        priority (str): Priority level of the task (low, medium, high).
        due_date (datetime): Optional due date and time for the task.
        status (str): Current status of the task (pending, in progress, completed).
        categories (ManyToMany): Categories the task belongs to.
        user (ForeignKey): The user who owns the task.
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.
    """

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    categories = models.ManyToManyField(Category, related_name='tasks', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
