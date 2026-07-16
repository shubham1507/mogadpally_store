from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Address
from .validators import validate_user_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Used for:
    - Registration response
    - Profile API
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "role",
            "is_verified",
            "profile_image",
            "date_of_birth",
        ]
        read_only_fields = [
            "id",
            "role",
            "is_verified",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
    )

    confirm_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "phone",
        ]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value.lower()

    def validate_phone(self, value):
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password": "Passwords do not match."
                }
            )

        validate_user_password(attrs["password"])

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone=validated_data.get("phone"),
        )

        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ["user"]

    def validate(self, attrs):
        """
        Ensure only one default address exists.
        """
        if attrs.get("is_default"):
            user = self.context["request"].user

            Address.objects.filter(
                user=user,
                is_default=True,
            ).update(is_default=False)

        return attrs



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        RefreshToken(self.validated_data["refresh"]).blacklist()