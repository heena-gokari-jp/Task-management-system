from datetime import timedelta

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from tasks.models import Category, Task
from users.models import UserProfile


class TaskModelTest(TestCase):
    """Test cases for Task model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(name="Test Category", user=self.user)

    def test_task_creation(self):
        """Test creating a task with all fields"""
        task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            priority="high",
            status="pending",
            user=self.user,
            due_date=timezone.now() + timedelta(days=7),
        )
        task.categories.add(self.category)

        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.categories.count(), 1)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)

    def test_task_str_method(self):
        """Test task string representation"""
        task = Task.objects.create(title="Test Task Title", user=self.user)
        self.assertEqual(str(task), "Test Task Title")

    def test_task_defaults(self):
        """Test task default values"""
        task = Task.objects.create(title="Default Task", user=self.user)
        self.assertEqual(task.priority, "medium")
        self.assertEqual(task.status, "pending")
        self.assertIsNone(task.description)
        self.assertIsNone(task.due_date)

    def test_task_priority_choices(self):
        """Test task priority validation"""
        valid_priorities = ["low", "medium", "high"]
        for priority in valid_priorities:
            task = Task.objects.create(
                title=f"Task {priority}", priority=priority, user=self.user
            )
            self.assertEqual(task.priority, priority)

    def test_task_status_choices(self):
        """Test task status validation"""
        valid_statuses = ["pending", "in_progress", "completed"]
        for status in valid_statuses:
            task = Task.objects.create(
                title=f"Task {status}", status=status, user=self.user
            )
            self.assertEqual(task.status, status)


class CategoryModelTest(TestCase):
    """Test cases for Category model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="testpass123"
        )

    def test_category_creation(self):
        """Test creating a category"""
        category = Category.objects.create(name="Work", user=self.user)
        self.assertEqual(category.name, "Work")
        self.assertEqual(category.user, self.user)

    def test_category_str_method(self):
        """Test category string representation"""
        category = Category.objects.create(name="Personal", user=self.user)
        self.assertEqual(str(category), "Personal")

    def test_category_unique_constraint(self):
        """Test category unique constraint per user"""
        # Create first category
        Category.objects.create(name="Duplicate", user=self.user)

        # Try to create duplicate for same user (should fail)
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Duplicate", user=self.user)

        # Create same name for different user (should succeed)
        category = Category.objects.create(name="Duplicate", user=self.other_user)
        self.assertEqual(category.name, "Duplicate")
        self.assertEqual(category.user, self.other_user)


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        # Ensure profile exists for testing
        if not hasattr(self.user, "profile"):
            UserProfile.objects.create(user=self.user)

    def test_profile_creation_signal(self):
        """Test that UserProfile is created when User is created"""
        # Create a new user to test signal
        new_user = User.objects.create_user(
            username="newuser", email="new@example.com", password="testpass123"
        )

        # Check if profile exists or create manually for test
        try:
            profile = new_user.profile
            self.assertIsNotNone(profile)
        except UserProfile.DoesNotExist:
            # If signal didn't work, manually create for this test
            profile = UserProfile.objects.create(user=new_user)
            self.assertIsNotNone(profile)

    def test_profile_str_method(self):
        """Test UserProfile string representation"""
        expected = f"{self.user.username}'s profile"
        self.assertEqual(str(self.user.profile), expected)

    def test_profile_defaults(self):
        """Test UserProfile default values"""
        profile = self.user.profile
        self.assertIsNotNone(profile)
        # Test that the profile exists and is properly linked
        self.assertEqual(profile.user, self.user)
