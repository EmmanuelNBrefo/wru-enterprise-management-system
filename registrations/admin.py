from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "course",
        "academic_year",
        "semester",
        "status",
        "registered_at",
    )

    search_fields = (
        "student__student_id",
        "student__first_name",
        "student__last_name",
        "course__code",
        "course__title",
    )

    list_filter = (
        "academic_year",
        "semester",
        "status",
    )

    ordering = (
        "-registered_at",
    )