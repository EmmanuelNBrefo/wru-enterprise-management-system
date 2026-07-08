from django.contrib import admin
from .models import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Role model.
    """

    list_display = (
        "name",
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "name",
    )