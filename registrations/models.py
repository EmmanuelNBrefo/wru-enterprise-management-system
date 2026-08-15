from django.db import models

from students.models import Student
from courses.models import Course

class Registration(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    registration_no = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="registrations"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="registrations"
    )

    academic_year = models.CharField(
        max_length=20
    )

    semester = models.CharField(
        max_length=30
    )

    registration_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "course",
                    "academic_year",
                    "semester",
                ],
                name="unique_student_course_registration",
            )
        ]

    def save(self, *args, **kwargs):

        if not self.registration_no:

            if self.registration_date:
                year = self.registration_date.year
            else:
                from django.utils import timezone
                year = timezone.now().year

            last = Registration.objects.filter(
                registration_no__startswith=f"REG-{year}"
            ).count() + 1

            self.registration_no = (
                f"REG-{year}-{last:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.registration_no
