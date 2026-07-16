import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model for Mogadpally Brothers.

    Authentication:
    - Login using email
    - UUID primary key
    - Phone number as secondary unique identifier

    Future Ready:
    - Profile image
    - DOB
    - Roles
    - Email verification
    """

    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        STAFF = "staff", "Staff"
        ADMIN = "admin", "Admin"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        unique=True,
    )

    phone = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
    )

    profile_image = models.ImageField(
        upload_to="users/profile/",
        null=True,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    is_verified = models.BooleanField(
        default=False,
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    created_at = models.DateTimeField(
    auto_now_add=True,
    editable=False,
)

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class Address(models.Model):
    """
    Shipping/Billing Address
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    label = models.CharField(
        max_length=50,
        blank=True,
        help_text="Home, Office, etc.",
    )

    line1 = models.CharField(max_length=255)

    line2 = models.CharField(
        max_length=255,
        blank=True,
    )

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=20)

    country = models.CharField(
        max_length=100,
        default="India",
    )

    is_default = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
       auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-is_default", "-created_at"]
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.user.email} - {self.label or self.city}"