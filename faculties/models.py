from django.db import models


class Faculty(models.Model):
    """
    Represents a faculty or school within Western Region University.
    """

    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Faculty code (e.g. FST, FBA, FHS)"
    )

    name = models.CharField(
        max_length=150,
        unique=True,
        help_text="Official faculty name"
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
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"

    def __str__(self):
        return f"{self.code} - {self.name}"