from django.contrib import admin
from .models import Program


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "department",
        "duration_years",
        "is_active",
        "created_at",
    )

    search_fields = (
        "code",
        "name",
        "department__name",
    )

    list_filter = (
        "department",
        "is_active",
        "duration_years",
    )

    ordering = (
        "code",
    )