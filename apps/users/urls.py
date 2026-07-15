from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import SignupView, MeView, AddressViewSet

router = DefaultRouter()
router.register("me/addresses", AddressViewSet, basename="address")

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("login", TokenObtainPairView.as_view(), name="login"),
    path("refresh", TokenRefreshView.as_view(), name="refresh"),
    path("me", MeView.as_view(), name="me"),
] + router.urls
