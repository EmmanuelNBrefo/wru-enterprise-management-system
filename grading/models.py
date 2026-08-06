from django.core.exceptions import ValidationError
from django.db import models


class GradeRule(models.Model):

    grade = models.CharField(
        max_length=5
    )

    minimum_score = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    maximum_score = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    grade_point = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    description = models.CharField(
        max_length=100,
        blank=True
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

    def clean(self):

        if self.minimum_score < 0:
            raise ValidationError(
                "Minimum score cannot be below 0."
            )

        if self.maximum_score > 100:
            raise ValidationError(
                "Maximum score cannot exceed 100."
            )

        if self.minimum_score > self.maximum_score:
            raise ValidationError(
                "Minimum score cannot be greater than maximum score."
            )

    class Meta:
        ordering = [
            "-minimum_score"
        ]

    def __str__(self):
        return (
            f"{self.grade} "
            f"({self.minimum_score}-{self.maximum_score})"
        )