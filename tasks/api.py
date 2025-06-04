from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """API endpoint for tasks."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only tasks owned by the current user."""
        try:
            return Task.objects.filter(user=self.request.user)
        except Exception as e:
            return Response(
                {"error": f"Error retrieving tasks: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def perform_create(self, serializer):
        """Set the user when creating a task."""
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response(
                {"error": f"Error creating task: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for categories."""

    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only categories owned by the current user."""
        try:
            return Category.objects.filter(user=self.request.user)
        except Exception as e:
            return Response(
                {"error": f"Error retrieving categories: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def perform_create(self, serializer):
        """Set the user when creating a category."""
        try:
            serializer.save(user=self.request.user)
        except Exception as e:
            return Response(
                {"error": f"Error creating category: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
