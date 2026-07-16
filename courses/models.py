from django.db import models
from departments.models import Department


class Course(models.Model):
    """
    Represents an academic course offered by WRU.
    """

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="courses"
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Course code e.g. IT101"
    )

    title = models.CharField(
        max_length=150,
        help_text="Course title"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    credit_hours = models.PositiveIntegerField(
        default=3
    )

    level = models.CharField(
        max_length=20,
        help_text="Example: 100, 200, 300, 400"
    )

    semester = models.CharField(
        max_length=20,
        help_text="Example: First Semester"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        ordering = ["code"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"


    def __str__(self):
        return f"{self.code} - {self.title}"