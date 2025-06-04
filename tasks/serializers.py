from rest_framework import serializers

from .models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    This serializer handles the conversion of Category model instances to and from JSON format,
    typically for API responses and requests. Only the 'id' and 'name' fields are writable,
    while the 'user' field is marked as read-only to prevent client-side modification.
    """

    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["user"]


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    This serializer is used to convert Task model instances into JSON format for API responses,
    and to validate and save JSON input data into Task model instances. It includes fields such as
    task title, description, priority, due date, status, and related categories. The 'user',
    'created_at', and 'updated_at' fields are read-only.

    Fields:
        id (int): Unique identifier of the task.
        title (str): Title or name of the task.
        description (str): Optional detailed description of the task.
        priority (int): Integer value indicating the task's priority.
        due_date (datetime): Date and time by which the task should be completed.
        status (str): Current status of the task (e.g., 'pending', 'completed').
        categories (list): List of categories the task belongs to (many-to-many).
        created_at (datetime): Timestamp when the task was created.
        updated_at (datetime): Timestamp when the task was last updated.
    """

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "due_date",
            "status",
            "categories",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]
