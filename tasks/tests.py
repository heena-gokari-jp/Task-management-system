from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Category

class TaskModelTest(TestCase):
    """Test suite for the Task model."""

    def setUp(self):
        """Set up test user, category, and task."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name='Test Category',
            user=self.user
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            priority='high',
            status='pending',
            user=self.user
        )
        self.task.categories.add(self.category)

    def test_task_creation(self):
        """Test the creation of a Task object."""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.priority, 'high')
        self.assertEqual(self.task.status, 'pending')
        self.assertEqual(self.task.user, self.user)
        self.assertEqual(self.task.categories.count(), 1)
        self.assertEqual(self.task.categories.first(), self.category)

class TaskViewsTest(TestCase):
    """Test suite for Task views."""

    def setUp(self):
        """Log in test user and create initial data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.category = Category.objects.create(
            name='Test Category',
            user=self.user
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            priority='high',
            status='pending',
            user=self.user
        )
        self.task.categories.add(self.category)

    def test_task_list_view(self):
        """Test task list page loads and contains expected content."""
        response = self.client.get(reverse('tasks:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_detail_view(self):
        """Test task detail page content."""
        response = self.client.get(reverse('tasks:task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        self.assertContains(response, 'Test Description')

    def test_task_create_view(self):
        """Test creating a new task via POST request."""
        response = self.client.post(reverse('tasks:task_create'), {
            'title': 'New Task',
            'description': 'New Description',
            'priority': 'medium',
            'status': 'in_progress',
            'categories': [self.category.id]
        })
        self.assertEqual(Task.objects.count(), 2)
        new_task = Task.objects.get(title='New Task')
        self.assertEqual(new_task.description, 'New Description')
        self.assertEqual(new_task.priority, 'medium')
        self.assertEqual(new_task.status, 'in_progress')

    def test_task_update_view(self):
        """Test updating an existing task."""
        response = self.client.post(reverse('tasks:task_update', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'priority': 'low',
            'status': 'completed',
            'categories': [self.category.id]
        })
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertEqual(self.task.priority, 'low')
        self.assertEqual(self.task.status, 'completed')

    def test_task_delete_view(self):
        """Test deleting a task."""
        response = self.client.post(reverse('tasks:task_delete', args=[self.task.id]))
        self.assertEqual(Task.objects.count(), 0)
