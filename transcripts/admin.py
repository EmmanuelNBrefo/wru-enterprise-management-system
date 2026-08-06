from django.contrib import admin
from .models import Transcript


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "transcript_type",
        "status",
        "is_official",
        "generated_at",
    )

    search_fields = (
        "student__student_id",
        "student__first_name",
        "student__last_name",
        "verification_code",
    )

    list_filter = (
        "status",
        "is_official",
        "transcript_type",
    )

    readonly_fields = (
        "verification_code",
        "generated_at",
    )

    ordering = (
        "-generated_at",
    )