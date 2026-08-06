from django.contrib import admin
from .models import GradeRule


@admin.register(GradeRule)
class GradeRuleAdmin(admin.ModelAdmin):

    list_display = (
        "grade",
        "minimum_score",
        "maximum_score",
        "grade_point",
        "is_active",
    )

    search_fields = (
        "grade",
        "description",
    )

    list_filter = (
        "grade",
        "is_active",
    )

    ordering = (
        "-minimum_score",
    )