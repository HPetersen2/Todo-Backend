from rest_framework import generics
from todo_app.models import Todo
from .permissions import IsAuthenticatedWithCookie
from .serializers import TodoSerializer

class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedWithCookie]

    def get_queryset(self):
        """
        Returns a queryset containing only todo items created by the authenticated user.
        """
        return Todo.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        """
        Persists a new todo item while assigning the authenticated user as its creator.
        """
        serializer.save(creator=self.request.user)

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedWithCookie]

    def get_queryset(self):
        """
        Restricts access to todo items so that only those owned by the authenticated user are exposed.
        """
        return Todo.objects.filter(creator=self.request.user)
