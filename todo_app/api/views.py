from rest_framework import generics
from todo_app.models import Todo
from .permissions import IsAuthenticatedWithCookie
from .serializers import TodoSerializer

class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedWithCookie]

    def get_queryset(self):
        return Todo.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedWithCookie]

    def get_queryset(self):
        return Todo.objects.filter(creator=self.request.user)