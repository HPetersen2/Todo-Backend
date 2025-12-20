from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Register a user using username and password (account active immediately)."""
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True}
        }

    def validate_confirmed_password(self, value):
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value

    def save(self):
        pw = self.validated_data['password']
        account = User(username=self.validated_data['username'])
        account.is_active = True
        account.set_password(pw)
        account.save()
        return account


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Thin wrapper around the default serializer using username/password."""
    pass
