from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    program_name = serializers.CharField(
        source="program.name",
        read_only=True
    )

    level = serializers.CharField(
        source="current_level",
        read_only=True
    )

    class Meta:
        model = Student
        fields = [
            "student_id",

            "name",
            "program_name",
            "level",
            "status",

            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "date_of_birth",
            "email",
            "phone",
            "address",

            "program",
            "admission_year",
            "current_level",
        ]

    def get_name(self, obj):
        if obj.middle_name:
            return f"{obj.first_name} {obj.middle_name} {obj.last_name}"

        return f"{obj.first_name} {obj.last_name}"


class StudentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "gender",
            "date_of_birth",
            "email",
            "phone",
            "address",
            "program",
            "admission_year",
            "current_level",
            "status",
        ]