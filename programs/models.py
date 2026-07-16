from django.db import models
from departments.models import Department


class Program(models.Model):
    """
    Represents an academic program offered by Western Region University.
    """

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="programs"
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Program code (example: BIT, BCSC)"
    )

    name = models.CharField(
        max_length=150,
        unique=True,
        help_text="Official program name"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    duration_years = models.PositiveIntegerField(
        default=4,
        help_text="Normal duration of the program"
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
        verbose_name = "Program"
        verbose_name_plural = "Programs"

    def __str__(self):
        return f"{self.code} - {self.name}"