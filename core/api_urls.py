from django.urls import path, include

"""
Aggregates API URL configurations from authentication and todo application modules under the root API path.
"""
urlpatterns = [
    path('', include('auth_app.api.urls')),
    path('', include('todo_app.api.urls')),
]