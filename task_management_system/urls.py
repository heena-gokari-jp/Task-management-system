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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from tasks.api import TaskViewSet, CategoryViewSet

# API router setup
router = routers.DefaultRouter()
# router.register(r'tasks', TaskViewSet)
# In task_management_system/urls.py
router.register(r'tasks', TaskViewSet, basename='task')  # Added basename parameter
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('tasks/', include('tasks.urls')),
    path('users/', include('users.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]




# # In task_management_system/urls.py
# from django.urls import path, include
# from django.contrib import admin
# from django.views.generic import TemplateView, RedirectView
# from rest_framework import routers
# from tasks.api import TaskViewSet, CategoryViewSet

# # API router setup
# router = routers.DefaultRouter()
# router.register(r'tasks', TaskViewSet, basename='task')
# router.register(r'categories', CategoryViewSet, basename='category')

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/', include('allauth.urls')),
#     path('tasks/', include('tasks.urls')),
#     path('users/', include('users.urls')),
#     path('api/', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls')),
#     path('dashboard/', RedirectView.as_view(pattern_name='tasks:task_list'), name='dashboard'),  # Add this line
#     path('', TemplateView.as_view(template_name='home.html'), name='home'),
# ]
