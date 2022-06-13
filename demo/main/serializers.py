from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class ResendVerificationEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    tokens = serializers.CharField(max_length=68, min_length=8, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid Login Credentials, try again!')
        if not user.is_active:
            raise AuthenticationFailed('Your Acccount is disabled, please contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Your Email is not verified')

        return {
            'email': user.email,
            'tokens': user.get_tokens
        }