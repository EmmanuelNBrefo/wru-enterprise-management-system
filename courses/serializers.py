from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):

    department_name = serializers.CharField(
        source="department.name",
        read_only=True
    )

    class Meta:
        model = Course

        fields = [
            "id",
            "department",
            "department_name",
            "code",
            "title",
            "description",
            "credit_hours",
            "level",
            "semester",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]