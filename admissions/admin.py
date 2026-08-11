from django.contrib import admin
from .models import Admission


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):

    list_display = (
        "admission_no",
        "student",
        "academic_year",
        "semester",
        "status",
    )

    search_fields = (
        "admission_no",
        "student__student_id",
        "student__first_name",
        "student__last_name",
    )

    list_filter = (
        "academic_year",
        "semester",
        "status",
    )