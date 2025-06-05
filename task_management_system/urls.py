"""
URL configuration for task_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from rest_framework import routers

from django.contrib import admin

# # In task_management_system/urls.py
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

from tasks import views
from tasks.api import CategoryViewSet, TaskViewSet

# API router setup
router = routers.DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("tasks/", include("tasks.urls")),
    path("users/", include("users.urls")),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path(
        "dashboard/",
        RedirectView.as_view(pattern_name="tasks:task_list"),
        name="dashboard",
    ),  # Add this line
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    # Task management
    path("", views.task_list, name="task_list"),
    path("create/", views.task_create, name="task_create"),
    path("<int:pk>/", views.task_detail, name="task_detail"),
    path("<int:pk>/update/", views.task_update, name="task_update"),
    path("<int:pk>/delete/", views.task_delete, name="task_delete"),
    # Categories
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    # Notifications
    path("notifications/", views.task_notifications, name="notifications"),
    path(
        "api/notifications-count/",
        views.notifications_count,
        name="notifications_count",
    ),
    path("api/dashboard-stats/", views.task_dashboard_stats, name="dashboard_stats"),
]
