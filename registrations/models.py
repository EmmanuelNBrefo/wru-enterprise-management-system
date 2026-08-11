from django.db import models

from students.models import Student


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

    def save(self, *args, **kwargs):

        if not self.registration_no:

            year = self.registration_date.year

            last = Registration.objects.filter(
                registration_no__startswith=f"REG-{year}"
            ).count() + 1

            self.registration_no = (
                f"REG-{year}-{last:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.registration_no