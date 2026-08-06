from django.contrib import admin
from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = (
        "registration",
        "score",
        "grade",
        "grade_point",
        "created_at",
    )

    search_fields = (
        "registration__student__student_id",
        "registration__student__first_name",
        "registration__student__last_name",
        "registration__course__code",
    )

    list_filter = (
        "grade",
        "registration__semester",
        "registration__academic_year",
    )

    ordering = (
        "-created_at",
    )