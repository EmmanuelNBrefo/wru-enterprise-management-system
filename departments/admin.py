from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "name",
        "faculty",
        "is_active",
        "created_at",
    )

    search_fields = (
        "code",
        "name",
        "faculty__name",
    )

    list_filter = (
        "faculty",
        "is_active",
    )

    ordering = (
        "code",
    )