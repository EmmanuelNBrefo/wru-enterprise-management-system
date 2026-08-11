from rest_framework import serializers

from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):

    student_name = serializers.SerializerMethodField()
    student_id = serializers.CharField(
        source="student.student_id",
        read_only=True
    )
    program_name = serializers.CharField(
        source="student.program.name",
        read_only=True
    )
    current_level = serializers.CharField(
        source="student.current_level",
        read_only=True
    )

    class Meta:
        model = Registration

        fields = [
            "registration_no",

            "student",
            "student_id",
            "student_name",
            "program_name",
            "current_level",

            "academic_year",
            "semester",
            "registration_date",
            "status",
            "remarks",

            "created_at",
        ]

        read_only_fields = [
            "registration_no",
            "created_at",
        ]

    def get_student_name(self, obj):
        student = obj.student

        if student.middle_name:
            return (
                f"{student.first_name} "
                f"{student.middle_name} "
                f"{student.last_name}"
            )

        return (
            f"{student.first_name} "
            f"{student.last_name}"
        )