from rest_framework import serializers
from .models import Admission


class AdmissionSerializer(serializers.ModelSerializer):

    student_name = serializers.SerializerMethodField()

    student_id = serializers.CharField(
        source="student.student_id",
        read_only=True
    )

    class Meta:
        model = Admission

        fields = [
            "id",
            "admission_no",

            "student",
            "student_id",
            "student_name",

            "admission_date",
            "academic_year",
            "semester",
            "status",
            "remarks",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "admission_no",
            "student_id",
            "student_name",
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