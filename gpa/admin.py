from django.contrib import admin
from .models import GPARecord


@admin.register(GPARecord)
class GPARecordAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "academic_year",
        "semester",
        "total_credit_hours",
        "total_quality_points",
        "gpa",
        "calculated_at",
    )

    search_fields = (
        "student__student_id",
        "student__first_name",
        "student__last_name",
    )

    list_filter = (
        "academic_year",
        "semester",
    )

    ordering = (
        "-academic_year",
        "semester",
    )