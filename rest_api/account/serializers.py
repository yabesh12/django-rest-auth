from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            credentials = {
                'email': email,
                'password': password
            }
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                return {
                    'email': user.email,
                    'refresh': str(refresh),
                    'access': str(access_token),
                }
            else:
                raise serializers.ValidationError("Incorrect Login credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")


from rest_framework_simplejwt.serializers import TokenObtainSerializer

class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.EMAIL_FIELD