from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


def validate_user_password(password):
    """
    Runs Django's built-in password validators.
    Raises ValidationError if password is weak.
    """
    try:
        validate_password(password)
    except Exception as exc:
        raise serializers.ValidationError(list(exc.messages))