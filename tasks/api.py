from rest_framework import viewsets, permissions
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer

class TaskViewSet(viewsets.ModelViewSet):
    """API endpoint for tasks."""
    queryset = Task.objects.all() 
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only tasks owned by the current user."""
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user when creating a task."""
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for categories."""
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only categories owned by the current user."""
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Set the user when creating a category."""
        serializer.save(user=self.request.user)
