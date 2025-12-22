from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

def jwt_user(request):
    """
    Extracts and returns the authenticated user from a JWT access token stored in cookies, or None if validation fails.
    """
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(request.COOKIES.get('access_token'))
        user = jwt_authenticator.get_user(validated_token)
        return {'jwt_user': user} if user and user.is_authenticated else {'jwt_user': None}
    except (InvalidToken, TokenError):
        return {'jwt_user': None}
