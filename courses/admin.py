from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "title",
        "department",
        "credit_hours",
        "level",
        "semester",
        "is_active",
        "created_at",
    )

    search_fields = (
        "code",
        "title",
        "department__name",
    )

    list_filter = (
        "department",
        "level",
        "semester",
        "is_active",
    )

    ordering = (
        "code",
    )