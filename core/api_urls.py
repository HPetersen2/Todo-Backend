from django.urls import path, include

urlpatterns = [
    path('', include('todo_app.api.urls')),
]