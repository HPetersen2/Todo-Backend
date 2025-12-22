from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, TokenRefreshView

app_name = 'auth_app'

"""
Sets up API endpoints for user registration, login, logout, and JWT token refresh operations.
"""
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
