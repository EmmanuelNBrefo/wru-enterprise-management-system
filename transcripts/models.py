from decimal import Decimal, ROUND_HALF_UP
import secrets

from django.db import models

from students.models import Student
from registrations.models import Registration


class Transcript(models.Model):

    # ----------------------------------------
    # STATUS OPTIONS
    # ----------------------------------------

    STATUS_PENDING = "PENDING"
    STATUS_ACTIVE = "ACTIVE"
    STATUS_REVOKED = "REVOKED"
    STATUS_EXPIRED = "EXPIRED"

    STATUS_CHOICES = [

        (
            STATUS_PENDING,
            "Pending"
        ),

        (
            STATUS_ACTIVE,
            "Active"
        ),

        (
            STATUS_REVOKED,
            "Revoked"
        ),

        (
            STATUS_EXPIRED,
            "Expired"
        ),

    ]

    # ----------------------------------------
    # STUDENT
    # ----------------------------------------

    student = models.ForeignKey(

        Student,

        on_delete=models.PROTECT,

        related_name="transcripts"

    )

    # ----------------------------------------
    # TRANSCRIPT INFORMATION
    # ----------------------------------------

    transcript_type = models.CharField(

        max_length=30,

        default="Official Transcript"

    )

    generated_at = models.DateTimeField(

        auto_now_add=True

    )

    is_official = models.BooleanField(

        default=False

    )

    # ----------------------------------------
    # TRANSCRIPT STATUS
    # ----------------------------------------

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default=STATUS_PENDING

    )

    # ----------------------------------------
    # VERIFICATION CODE
    # ----------------------------------------

    verification_code = models.CharField(

        max_length=30,

        unique=True,

        editable=False,

        blank=True

    )

    # ----------------------------------------
    # OFFICIAL INFORMATION
    # ----------------------------------------

    registrar_name = models.CharField(

        max_length=150,

        blank=True,

        null=True

    )

    dean_name = models.CharField(

        max_length=150,

        blank=True,

        null=True

    )

    # ----------------------------------------
    # NOTES
    # ----------------------------------------

    notes = models.TextField(

        blank=True,

        null=True

    )

    # ----------------------------------------
    # VERIFICATION CODE GENERATOR
    # ----------------------------------------

    def generate_verification_code(self):

        return (

            "WRU-TR-"

            f"{secrets.token_hex(6).upper()}"

        )

    # ----------------------------------------
    # SAVE
    # ----------------------------------------

    def save(self, *args, **kwargs):

        if not self.verification_code:

            self.verification_code = (

                self.generate_verification_code()

            )

        super().save(*args, **kwargs)

    # ----------------------------------------
    # STATUS HELPERS
    # ----------------------------------------

    def is_valid(self):

        return (

            self.status == self.STATUS_ACTIVE

            and self.is_official

        )

    def is_revoked(self):

        return (

            self.status == self.STATUS_REVOKED

        )

    def is_expired(self):

        return (

            self.status == self.STATUS_EXPIRED

        )

    def get_status_display_name(self):

        return dict(

            self.STATUS_CHOICES

        ).get(

            self.status,

            self.status

        )

    # ----------------------------------------
    # ACADEMIC RECORDS
    # ----------------------------------------

    def get_academic_records(self):

        registrations = (

            Registration.objects

            .filter(

                student=self.student

            )

            .select_related(

                "course"

            )

            .prefetch_related(

                "result"

            )

            .order_by(

                "academic_year",

                "semester",

                "course__code"

            )

        )

        academic_records = []

        for registration in registrations:

            result = getattr(

                registration,

                "result",

                None

            )

            academic_records.append({

                "academic_year": (

                    registration.academic_year

                ),

                "semester": (

                    registration.semester

                ),

                "course_code": (

                    registration.course.code

                ),

                "course_title": (

                    registration.course.title

                ),

                "credit_hours": (

                    registration.course.credit_hours

                ),

                "score": (

                    result.score

                    if result

                    else None

                ),

                "grade": (

                    result.grade

                    if result

                    else None

                ),

                "grade_point": (

                    result.grade_point

                    if result

                    else None

                ),

            })

        return academic_records

    # ----------------------------------------
    # GPA CALCULATION
    # ----------------------------------------

    def calculate_gpa(

        self,

        academic_year=None,

        semester=None

    ):

        registrations = (

            Registration.objects

            .filter(

                student=self.student

            )

            .select_related(

                "course"

            )

            .prefetch_related(

                "result"

            )

        )

        if academic_year:

            registrations = (

                registrations.filter(

                    academic_year=academic_year

                )

            )

        if semester:

            registrations = (

                registrations.filter(

                    semester=semester

                )

            )

        total_credit_hours = Decimal(

            "0.00"

        )

        total_quality_points = Decimal(

            "0.00"

        )

        for registration in registrations:

            result = getattr(

                registration,

                "result",

                None

            )

            if not result:

                continue

            if result.grade_point is None:

                continue

            credit_hours = Decimal(

                str(

                    registration.course.credit_hours

                )

            )

            grade_point = Decimal(

                str(

                    result.grade_point

                )

            )

            total_credit_hours += (

                credit_hours

            )

            total_quality_points += (

                grade_point

                * credit_hours

            )

        if total_credit_hours == 0:

            return {

                "total_credit_hours": Decimal(

                    "0.00"

                ),

                "total_quality_points": Decimal(

                    "0.00"

                ),

                "gpa": Decimal(

                    "0.00"

                ),

            }

        gpa = (

            total_quality_points

            / total_credit_hours

        ).quantize(

            Decimal(

                "0.01"

            ),

            rounding=ROUND_HALF_UP

        )

        return {

            "total_credit_hours": (

                total_credit_hours

            ),

            "total_quality_points": (

                total_quality_points

            ),

            "gpa": gpa,

        }

    # ----------------------------------------
    # ACADEMIC STANDING
    # ----------------------------------------

    def get_academic_standing(self):

        gpa = self.calculate_gpa()["gpa"]

        if gpa >= Decimal("3.50"):

            return "Excellent"

        if gpa >= Decimal("2.00"):

            return "Good Standing"

        if gpa >= Decimal("1.50"):

            return "Academic Warning"

        return "Academic Probation"

    # ----------------------------------------
    # SEMESTER SUMMARIES
    # ----------------------------------------

    def get_semester_summaries(self):

        records = self.get_academic_records()

        periods = []

        for record in records:

            period = (

                record["academic_year"],

                record["semester"]

            )

            if period not in periods:

                periods.append(period)

        summaries = []

        for academic_year, semester in periods:

            gpa = self.calculate_gpa(

                academic_year=academic_year,

                semester=semester

            )

            summaries.append({

                "academic_year": (

                    academic_year

                ),

                "semester": (

                    semester

                ),

                "total_credit_hours": (

                    gpa[

                        "total_credit_hours"

                    ]

                ),

                "total_quality_points": (

                    gpa[

                        "total_quality_points"

                    ]

                ),

                "gpa": (

                    gpa["gpa"]

                ),

            })

        return summaries

    # ----------------------------------------
    # TRANSCRIPT SUMMARY
    # ----------------------------------------

    def get_transcript_summary(self):

        cumulative_gpa = (

            self.calculate_gpa()

        )

        return {

            "transcript": self,

            "student": self.student,

            "academic_records": (

                self.get_academic_records()

            ),

            "semester_summaries": (

                self.get_semester_summaries()

            ),

            "cumulative_gpa": (

                cumulative_gpa

            ),

            "academic_standing": (

                self.get_academic_standing()

            ),

            "status": (

                self.status

            ),

            "status_display": (

                self.get_status_display_name()

            ),

            "is_valid": (

                self.is_valid()

            ),

        }

    # ----------------------------------------
    # META
    # ----------------------------------------

    class Meta:

        ordering = [

            "-generated_at"

        ]

    # ----------------------------------------
    # STRING REPRESENTATION
    # ----------------------------------------

    def __str__(self):

        return (

            f"{self.transcript_type} - "

            f"{self.student.student_id}"

        )