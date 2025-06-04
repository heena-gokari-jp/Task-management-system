from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Category, Task


class TaskAPITest(TestCase):
    """Test cases for Task API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="testpass123"
        )
        self.category = Category.objects.create(name="Test Category", user=self.user)
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            priority="high",
            status="pending",
            user=self.user,
        )
        self.task.categories.add(self.category)

    def test_task_list_authenticated(self):
        """Test task list API for authenticated user"""
        self.client.force_authenticate(user=self.user)
        url = reverse("task-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Test Task")

    def test_task_list_unauthenticated(self):
        """Test task list API for unauthenticated user"""
        url = reverse("task-list")
        response = self.client.get(url)

        # Django REST Framework returns 403 by default, not 401
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_create_authenticated(self):
        """Test task creation via API"""
        self.client.force_authenticate(user=self.user)
        url = reverse("task-list")

        data = {
            "title": "New API Task",
            "description": "Created via API",
            "priority": "medium",
            "status": "pending",
            "category_ids": [self.category.id],
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

        new_task = Task.objects.get(title="New API Task")
        self.assertEqual(new_task.user, self.user)

    def test_task_update_authenticated(self):
        """Test task update via API"""
        self.client.force_authenticate(user=self.user)
        url = reverse("task-detail", kwargs={"pk": self.task.pk})

        data = {
            "title": "Updated API Task",
            "description": "Updated via API",
            "priority": "low",
            "status": "completed",
            "category_ids": [self.category.id],
        }

        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_task = Task.objects.get(pk=self.task.pk)
        self.assertEqual(updated_task.title, "Updated API Task")
        self.assertEqual(updated_task.status, "completed")

    def test_task_delete_authenticated(self):
        """Test task deletion via API"""
        self.client.force_authenticate(user=self.user)
        url = reverse("task-detail", kwargs={"pk": self.task.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_isolation_between_users(self):
        """Test that users can only access their own tasks via API"""
        # Create task for other user
        other_task = Task.objects.create(title="Other User Task", user=self.other_user)

        self.client.force_authenticate(user=self.user)

        # List tasks - should only see own task
        url = reverse("task-list")
        response = self.client.get(url)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Test Task")

        # Try to access other user's task
        url = reverse("task-detail", kwargs={"pk": other_task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
