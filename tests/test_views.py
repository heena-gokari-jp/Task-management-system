from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from tasks.models import Category, Task


class TaskViewsTest(TestCase):
    """Test cases for Task views"""

    def setUp(self):
        self.client = Client()
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
        """Test task list view for authenticated user"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("tasks:task_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Task")
        self.assertContains(response, self.task.title)

    def test_task_list_unauthenticated(self):
        """Test task list redirects unauthenticated users"""
        response = self.client.get(reverse("tasks:task_list"))
        self.assertRedirects(response, "/accounts/login/?next=/tasks/")

    def test_task_detail_view(self):
        """Test task detail view"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("tasks:task_detail", args=[self.task.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.title)
        self.assertContains(response, self.task.description)

    def test_task_detail_other_user(self):
        """Test user cannot view other user's tasks"""
        self.client.login(username="otheruser", password="testpass123")
        response = self.client.get(reverse("tasks:task_detail", args=[self.task.id]))

        self.assertEqual(response.status_code, 404)

    def test_task_create_get(self):
        """Test task create form display"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("tasks:task_create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Task")

    def test_task_create_post_valid(self):
        """Test creating a task with valid data"""
        self.client.login(username="testuser", password="testpass123")

        task_data = {
            "title": "New Task",
            "description": "New Description",
            "priority": "medium",
            "status": "pending",
            "categories": [self.category.id],
        }

        response = self.client.post(reverse("tasks:task_create"), task_data)
        self.assertRedirects(response, reverse("tasks:task_list"))

        # Check task was created
        self.assertTrue(Task.objects.filter(title="New Task").exists())
        new_task = Task.objects.get(title="New Task")
        self.assertEqual(new_task.user, self.user)
        self.assertEqual(new_task.description, "New Description")

    def test_task_update_post(self):
        """Test updating a task"""
        self.client.login(username="testuser", password="testpass123")

        update_data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "priority": "low",
            "status": "completed",
            "categories": [self.category.id],
        }

        response = self.client.post(
            reverse("tasks:task_update", args=[self.task.id]), update_data
        )

        self.assertRedirects(
            response, reverse("tasks:task_detail", args=[self.task.id])
        )

        # Check task was updated
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.status, "completed")

    def test_task_delete(self):
        """Test deleting a task"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(reverse("tasks:task_delete", args=[self.task.id]))
        self.assertRedirects(response, reverse("tasks:task_list"))

        # Check task was deleted
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_dashboard_view(self):
        """Test dashboard view"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("tasks:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")


class CategoryViewsTest(TestCase):
    """Test cases for Category views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(name="Test Category", user=self.user)

    def test_category_list_view(self):
        """Test category list view"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("tasks:category_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Category")

    def test_category_create_post(self):
        """Test creating a category"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("tasks:category_create"), {"name": "New Category"}
        )

        self.assertRedirects(response, reverse("tasks:category_list"))
        self.assertTrue(Category.objects.filter(name="New Category").exists())

    def test_category_delete(self):
        """Test deleting a category"""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            reverse("tasks:category_delete", args=[self.category.id])
        )
        self.assertRedirects(response, reverse("tasks:category_list"))

        self.assertFalse(Category.objects.filter(id=self.category.id).exists())


class UserViewsTest(TestCase):
    """Test cases for User views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_profile_view(self):
        """Test user profile view"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")
        self.assertContains(response, "test@example.com")

    def test_profile_update_post(self):
        """Test updating user profile"""
        self.client.login(username="testuser", password="testpass123")

        update_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "Name",
        }

        response = self.client.post(reverse("users:profile_update"), update_data)
        self.assertRedirects(response, reverse("users:profile"))

        # Check user was updated
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.email, "updated@example.com")
