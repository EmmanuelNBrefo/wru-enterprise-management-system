from decimal import Decimal, ROUND_HALF_UP

from django.db import models

from students.models import Student
from results.models import Result


class GPARecord(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="gpa_records"
    )

    academic_year = models.CharField(
        max_length=20,
        help_text="Example: 2026/2027"
    )

    semester = models.CharField(
        max_length=20,
        help_text="Example: First Semester"
    )

    total_credit_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    total_quality_points = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    gpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0
    )

    calculated_at = models.DateTimeField(
        auto_now=True
    )

    def calculate_gpa(self):

        results = Result.objects.filter(
            registration__student=self.student,
            registration__academic_year=self.academic_year,
            registration__semester=self.semester,
            grade_point__isnull=False
        ).select_related(
            "registration__course"
        )

        total_credit_hours = Decimal("0.00")

        total_quality_points = Decimal("0.00")

        for result in results:

            credit_hours = Decimal(
                result.registration.course.credit_hours
            )

            grade_point = result.grade_point

            total_credit_hours += credit_hours

            total_quality_points += (
                grade_point * credit_hours
            )

        if total_credit_hours > 0:

            gpa = (
                total_quality_points / total_credit_hours
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

        else:

            gpa = Decimal("0.00")

        self.total_credit_hours = total_credit_hours

        self.total_quality_points = total_quality_points

        self.gpa = gpa

    def save(self, *args, **kwargs):

        self.calculate_gpa()

        super().save(*args, **kwargs)

    class Meta:

        ordering = [
            "-academic_year",
            "semester"
        ]

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "student",
                    "academic_year",
                    "semester",
                ],
                name="unique_student_gpa_period"
            )

        ]

    def __str__(self):

        return (
            f"{self.student.student_id} - "
            f"{self.academic_year} - "
            f"{self.semester}"
        )