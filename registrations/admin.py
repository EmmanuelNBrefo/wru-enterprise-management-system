from django.contrib import admin

from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = [
        "registration_no",
        "student",
        "academic_year",
        "semester",
        "registration_date",
        "status",
        "created_at",
    ]

    list_filter = [
        "academic_year",
        "semester",
        "status",
    ]

    search_fields = [
        "registration_no",
        "student__student_id",
        "student__first_name",
        "student__middle_name",
        "student__last_name",
    ]

    ordering = [
        "-created_at"
    ]