from rest_framework import serializers

from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):

    # ==========================================
    # STUDENT INFORMATION
    # ==========================================

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

    # ==========================================
    # COURSE INFORMATION
    # ==========================================

    course_code = serializers.CharField(
        source="course.code",
        read_only=True
    )

    course_title = serializers.CharField(
        source="course.title",
        read_only=True
    )

    course_credit_hours = serializers.IntegerField(
        source="course.credit_hours",
        read_only=True
    )

    course_level = serializers.CharField(
        source="course.level",
        read_only=True
    )

    course_semester = serializers.CharField(
        source="course.semester",
        read_only=True
    )

    # ==========================================
    # META
    # ==========================================

    class Meta:
        model = Registration

        fields = [
            # Registration
            "registration_no",

            # Student
            "student",
            "student_id",
            "student_name",
            "program_name",
            "current_level",

            # Course
            "course",
            "course_code",
            "course_title",
            "course_credit_hours",
            "course_level",
            "course_semester",

            # Registration details
            "academic_year",
            "semester",
            "registration_date",
            "status",
            "remarks",

            # System
            "created_at",
        ]

        read_only_fields = [
            "registration_no",
            "created_at",

            "student_id",
            "student_name",
            "program_name",
            "current_level",

            "course_code",
            "course_title",
            "course_credit_hours",
            "course_level",
            "course_semester",
        ]

    # ==========================================
    # STUDENT NAME
    # ==========================================

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

