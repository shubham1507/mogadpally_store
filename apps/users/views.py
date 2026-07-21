from django.contrib.auth import authenticate

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    LoginSerializer,
    LogoutSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "Registration successful.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    request=LoginSerializer,
    responses={200: UserSerializer},
)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        print("1. Request received")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        print("2. Serializer OK")
        print(serializer.validated_data)

        user = authenticate(
            request=request,
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        print("Authenticated user:", user)
        print("3. authenticate() finished")

        if user is None:
            print("4. Invalid credentials")

            return Response(
                {
                    "detail": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        print("5. User authenticated")

        refresh = RefreshToken.for_user(user)

        print("6. JWT generated")

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    request=LogoutSerializer,
    responses={200: None},
)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {
                "message": "Logged out successfully"
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user