from django.db import models
from students.models import Student


class Admission(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    admission_no = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="admission"
    )

    admission_date = models.DateField()

    academic_year = models.CharField(max_length=20)

    semester = models.CharField(max_length=20)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.admission_no:

            year = self.admission_date.year

            last = Admission.objects.filter(
                admission_no__startswith=f"ADM-{year}"
            ).count() + 1

            self.admission_no = (
                f"ADM-{year}-{last:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.admission_no