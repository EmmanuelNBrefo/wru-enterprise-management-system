from django.core.exceptions import ValidationError
from django.db import models

from registrations.models import Registration
from grading.models import GradeRule


class Result(models.Model):

    registration = models.OneToOneField(
        Registration,
        on_delete=models.PROTECT,
        related_name="result"
    )

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    grade = models.CharField(
        max_length=5,
        blank=True
    )

    grade_point = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def clean(self):

        if self.score < 0 or self.score > 100:
            raise ValidationError(
                "Score must be between 0 and 100."
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        grade_rule = GradeRule.objects.filter(
            minimum_score__lte=self.score,
            maximum_score__gte=self.score,
            is_active=True
        ).first()

        if grade_rule:

            self.grade = grade_rule.grade

            self.grade_point = (
                grade_rule.grade_point
            )

        else:

            self.grade = ""

            self.grade_point = None

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):

        return (
        f"{self.registration.student.student_id} - "
        f"{self.registration.registration_no}"
    )