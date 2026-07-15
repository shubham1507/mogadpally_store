from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Address
from .serializers import SignupSerializer, UserSerializer, AddressSerializer


class SignupView(generics.CreateAPIView):
    """POST /api/v1/auth/signup — creates a user. Email verification sent async (TODO: hook up email task)."""
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=201)


class MeView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/v1/auth/me"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class AddressViewSet(viewsets.ModelViewSet):
    """CRUD for the current user's addresses — mounted at /api/v1/auth/me/addresses"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
