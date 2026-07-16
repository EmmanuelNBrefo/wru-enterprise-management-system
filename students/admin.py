from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "student_id",
        "first_name",
        "last_name",
        "program",
        "current_level",
        "status",
        "created_at",
    )

    search_fields = (
        "student_id",
        "first_name",
        "last_name",
        "email",
    )

    list_filter = (
        "program",
        "current_level",
        "status",
    )

    ordering = (
        "student_id",
    )