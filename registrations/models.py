from django.db import models
from students.models import Student
from courses.models import Course


class Registration(models.Model):

    SEMESTER_CHOICES = (
        ("FIRST", "First Semester"),
        ("SECOND", "Second Semester"),
    )

    STATUS_CHOICES = (
        ("REGISTERED", "Registered"),
        ("DROPPED", "Dropped"),
        ("COMPLETED", "Completed"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="registrations"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="registrations"
    )

    academic_year = models.CharField(
        max_length=20,
        help_text="Example: 2026/2027"
    )

    semester = models.CharField(
        max_length=10,
        choices=SEMESTER_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="REGISTERED"
    )

    registered_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-registered_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "course",
                    "academic_year",
                    "semester",
                ],
                name="unique_student_course_registration"
            )
        ]

    def __str__(self):
        return (
            f"{self.student.student_id} - "
            f"{self.course.code} - "
            f"{self.academic_year}"
        )