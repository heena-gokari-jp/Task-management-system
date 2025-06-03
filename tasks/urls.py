from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='task_list'),  # List all tasks with filtering, sorting, and search
    path('create/', views.task_create, name='task_create'),  # Create a new task
    path('<int:pk>/', views.task_detail, name='task_detail'),  # View details of a specific task
    path('<int:pk>/update/', views.task_update, name='task_update'),  # Update an existing task
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),  # Delete a specific task
    path('categories/', views.category_list, name='category_list'),  # List all categories
    path('categories/create/', views.category_create, name='category_create'),  # Create a new category
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),  # Delete a specific category
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notifications/', views.task_notifications, name='notifications'),
    path('api/notifications-count/', views.notifications_count, name='notifications_count'),
    path('api/dashboard-stats/', views.task_dashboard_stats, name='dashboard_stats'),
]
