from django.db import models
from programs.models import Program
from django.utils import timezone


class Student(models.Model):

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("GRADUATED", "Graduated"),
        ("SUSPENDED", "Suspended"),
        ("WITHDRAWN", "Withdrawn"),
        ("DEFERRED", "Deferred"),
    )

    GENDER_CHOICES = (
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    )

    # Student Identity
    student_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        help_text="Auto generated or manually entered student ID"
    )

    first_name = models.CharField(
        max_length=100
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    last_name = models.CharField(
        max_length=100
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )


    # Contact Information
    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField(
        blank=True,
        null=True
    )


    # Academic Information
    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="students"
    )

    admission_year = models.PositiveIntegerField(
        default=timezone.now().year
    )

    current_level = models.CharField(
        max_length=20,
        default="100"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )


    # System Tracking
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:
        ordering = ["student_id"]
        verbose_name = "Student"
        verbose_name_plural = "Students"


    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"


    def save(self, *args, **kwargs):

        if not self.student_id:
            year = timezone.now().year

            last_student = Student.objects.filter(
                student_id__startswith=f"WRU-{year}"
            ).order_by(
                "-id"
            ).first()

            if last_student:
                last_number = int(
                    last_student.student_id.split("-")[-1]
                )
                new_number = last_number + 1
            else:
                new_number = 1

            self.student_id = (
                f"WRU-{year}-{new_number:04d}"
            )

        super().save(*args, **kwargs)