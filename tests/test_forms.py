from django.contrib.auth.models import User
from django.test import TestCase

from tasks.forms import CategoryForm, TaskForm
from tasks.models import Category
from users.forms import UserUpdateForm


class TaskFormTest(TestCase):
    """Test cases for TaskForm"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.category = Category.objects.create(name="Test Category", user=self.user)

    def test_task_form_valid_data(self):
        """Test TaskForm with valid data"""
        form_data = {
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high",
            "status": "pending",
            "categories": [self.category.id],
        }

        form = TaskForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_task_form_missing_title(self):
        """Test TaskForm with missing title"""
        form_data = {
            "description": "Test Description",
            "priority": "medium",
            "status": "pending",
        }

        form = TaskForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_task_form_invalid_priority(self):
        """Test TaskForm with invalid priority"""
        form_data = {"title": "Test Task", "priority": "invalid", "status": "pending"}

        form = TaskForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_task_form_category_filtering(self):
        """Test that TaskForm only shows user's categories"""
        other_user = User.objects.create_user(
            username="otheruser", email="other@example.com", password="testpass123"
        )
        other_category = Category.objects.create(name="Other Category", user=other_user)

        form = TaskForm(user=self.user)
        category_ids = [
            choice[0] for choice in form.fields["categories"].queryset.values_list("id")
        ]

        self.assertIn(self.category.id, category_ids)
        self.assertNotIn(other_category.id, category_ids)


class CategoryFormTest(TestCase):
    """Test cases for CategoryForm"""

    def test_category_form_valid_data(self):
        """Test CategoryForm with valid data"""
        form_data = {"name": "Work"}
        form = CategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_missing_name(self):
        """Test CategoryForm with missing name"""
        form_data = {}
        form = CategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)


class UserUpdateFormTest(TestCase):
    """Test cases for UserUpdateForm"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_user_update_form_valid_data(self):
        """Test UserUpdateForm with valid data"""
        form_data = {
            "username": "newusername",
            "email": "new@example.com",
            "first_name": "New",
            "last_name": "Name",
        }

        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_user_update_form_invalid_email(self):
        """Test UserUpdateForm with invalid email"""
        form_data = {
            "username": "testuser",
            "email": "invalid-email",
            "first_name": "Test",
            "last_name": "User",
        }

        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
