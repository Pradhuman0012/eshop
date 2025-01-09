from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(description="User registered successfully"),
            400: openapi.Response(description="Validation error"),
        },
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

from rest_framework_simplejwt.tokens import RefreshToken

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(description="Login successful"),
            401: openapi.Response(description="Invalid credentials"),
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Please provide both username and password."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful!",
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
