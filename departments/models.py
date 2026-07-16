from django.db import models
from faculties.models import Faculty

class Department(models.Model):

    faculty = models.ForeignKey(
    Faculty,
    on_delete=models.PROTECT,
    related_name="departments",
    null=True,
    blank=True
)
    """
    Represents an academic or administrative department
    within Western Region University.
    """

    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Department code (e.g. BIT, CSC, ACC)"
    )

    name = models.CharField(
        max_length=150,
        unique=True,
        help_text="Official department name"
    )

    description = models.TextField(
        blank=True,
        null=True
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
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return f"{self.code} - {self.name}"