import os

import pytest

import django
from django.conf import settings


def pytest_configure():
    """Configure Django settings for pytest."""
    if not settings.configured:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "task_management_system.settings"
        )
        django.setup()


@pytest.fixture
def user():
    """Create a test user"""
    from django.contrib.auth.models import User

    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def category(user):
    """Create a test category"""
    from tasks.models import Category

    return Category.objects.create(name="Test Category", user=user)


@pytest.fixture
def task(user, category):
    """Create a test task"""
    from tasks.models import Task

    task = Task.objects.create(
        title="Test Task",
        description="Test Description",
        priority="high",
        status="pending",
        user=user,
    )
    task.categories.add(category)
    return task
