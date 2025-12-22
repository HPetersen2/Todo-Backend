from django.urls import path
from .views import TodoListCreateView, TodoDetailView

"""
Configures API endpoints for listing, creating, retrieving, updating, and deleting todo resources.
"""
urlpatterns = [
    path('todos/', TodoListCreateView.as_view()),
    path('todos/<int:pk>/', TodoDetailView.as_view()),
]
