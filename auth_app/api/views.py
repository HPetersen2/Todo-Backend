from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer, CustomTokenObtainPairSerializer

User = get_user_model()


class RegistrationView(APIView):
    """Register a new user (account active immediately)."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            data = {
                "user": {
                    "id": account.pk,
                    "username": account.username,
                }
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    """Login using username and password; returns JWTs in cookies."""
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = serializer.validated_data
        username = request.data.get('username')
        user = None
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

        response = Response({
            "detail": "Login successful",
            "user": {"id": user.id, "username": user.username} if user else {},
        })

        # Tokens in HTTP-Only Cookies setzen
        access_token = tokens.get("access")
        refresh_token = tokens.get("refresh")

        # Access Token
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
        )

        # Refresh Token
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
        )

        return response



class LogoutView(APIView):
    """Logout by blacklisting provided refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get(
            'refresh') or request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "No refresh token provided."}, status=status.HTTP_200_OK)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Logout successful. Refresh token blacklisted."}, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    """Refresh access token using a refresh token provided in body or cookie."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        from rest_framework_simplejwt.serializers import TokenRefreshSerializer

        refresh = request.data.get(
            'refresh') or request.COOKIES.get('refresh_token')
        if not refresh:
            return Response({"detail": "Refresh token not found!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TokenRefreshSerializer(data={"refresh": refresh})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Refresh token invalid!"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
