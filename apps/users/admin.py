from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "phone", "role", "is_verified", "is_active")
    list_filter = ("role", "is_verified", "is_active")
    search_fields = ("email", "username", "phone")
    ordering = ("-date_joined",)


admin.site.register(Address)
