from django.contrib import admin
from .models import Faculty


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """
    Admin configuration for Faculty management.
    """

    list_display = (
        "code",
        "name",
        "is_active",
        "created_at",
    )

    search_fields = (
        "code",
        "name",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "code",
    )