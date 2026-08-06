from io import BytesIO

import qrcode

from django.conf import settings

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

from .models import Transcript


def generate_transcript_pdf(transcript_id):

    transcript = (
        Transcript.objects
        .select_related("student")
        .get(id=transcript_id)
    )

    report = transcript.get_transcript_summary()

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "UniversityTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=22,
        spaceAfter=5,
    )

    subtitle_style = ParagraphStyle(
        "TranscriptTitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        fontSize=14,
        leading=18,
        spaceAfter=10,
    )

    normal_style = styles["Normal"]

    story = []

    # ==================================================
    # UNIVERSITY HEADER
    # ==================================================

    story.append(
        Paragraph(
            "WESTERN REGION UNIVERSITY",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "WESTERN REGION UNIVERSITY OF LIBERIA",
            subtitle_style,
        )
    )

    story.append(
        Paragraph(
            "OFFICIAL ACADEMIC TRANSCRIPT",
            subtitle_style,
        )
    )

    story.append(
        Spacer(
            1,
            10,
        )
    )

    # ==================================================
    # STUDENT INFORMATION
    # ==================================================

    student = report["student"]

    student_name = (
        f"{student.first_name} "
        f"{student.middle_name or ''} "
        f"{student.last_name}"
    ).strip()

    student_data = [
        [
            Paragraph(
                "<b>Student ID:</b>",
                normal_style,
            ),

            student.student_id,

            Paragraph(
                "<b>Student Name:</b>",
                normal_style,
            ),

            student_name,
        ],

        [
            Paragraph(
                "<b>Program:</b>",
                normal_style,
            ),

            str(
                getattr(
                    student,
                    "program",
                    "",
                )
            ),

            Paragraph(
                "<b>Department:</b>",
                normal_style,
            ),

            str(
                getattr(
                    student,
                    "department",
                    "",
                )
            ),
        ],
    ]

    student_table = Table(
        student_data,
        colWidths=[
            30 * mm,
            55 * mm,
            35 * mm,
            55 * mm,
        ],
    )

    student_table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.whitesmoke,
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(student_table)

    story.append(
        Spacer(
            1,
            15,
        )
    )

    # ==================================================
    # ACADEMIC RECORDS
    # ==================================================

    academic_records = [
        [
            "Academic Year",
            "Semester",
            "Course Code",
            "Course Title",
            "Credits",
            "Score",
            "Grade",
            "Point",
        ]
    ]

    for record in report["academic_records"]:

        academic_records.append(
            [
                record["academic_year"],
                record["semester"],
                record["course_code"],
                record["course_title"],
                str(record["credit_hours"]),
                str(record["score"] or ""),
                record["grade"] or "",
                str(record["grade_point"] or ""),
            ]
        )

    academic_table = Table(
        academic_records,
        repeatRows=1,
        colWidths=[
            22 * mm,
            22 * mm,
            20 * mm,
            45 * mm,
            15 * mm,
            18 * mm,
            15 * mm,
            15 * mm,
        ],
    )

    academic_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f4e79"),
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),

                (
                    "ALIGN",
                    (4, 1),
                    (-1, -1),
                    "CENTER",
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7,
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    story.append(academic_table)

    story.append(
        Spacer(
            1,
            15,
        )
    )

    # ==================================================
    # GPA SUMMARY
    # ==================================================

    gpa = report["cumulative_gpa"]

    gpa_data = [
        [
            "Total Credit Hours",
            "Total Quality Points",
            "Cumulative GPA",
        ],

        [
            str(gpa["total_credit_hours"]),
            str(gpa["total_quality_points"]),
            str(gpa["gpa"]),
        ],
    ]

    gpa_table = Table(
        gpa_data,
        colWidths=[
            55 * mm,
            65 * mm,
            50 * mm,
        ],
    )

    gpa_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1f4e79"),
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(gpa_table)

    story.append(
        Spacer(
            1,
            20,
        )
    )

    # ==================================================
    # VERIFICATION QR CODE
    # ==================================================

    verification_code = transcript.verification_code

    verification_base_url = getattr(
        settings,
        "TRANSCRIPT_VERIFICATION_BASE_URL",
        "http://127.0.0.1:8000",
    ).rstrip("/")

    verification_url = (
        f"{verification_base_url}"
        f"/transcripts/verify/"
        f"{verification_code}/"
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=4,
    )

    qr.add_data(verification_url)

    qr.make(
        fit=True
    )

    qr_image = qr.make_image()

    qr_buffer = BytesIO()

    qr_image.save(
        qr_buffer,
        format="PNG",
    )

    qr_buffer.seek(0)

    qr_pdf_image = Image(
        qr_buffer,
        width=35 * mm,
        height=35 * mm,
    )

    verification_data = [
        [
            qr_pdf_image,

            [
                Paragraph(
                    "<b>TRANSCRIPT VERIFICATION</b>",
                    normal_style,
                ),

                Spacer(
                    1,
                    5,
                ),

                Paragraph(
                    f"<b>Verification Code:</b> "
                    f"{verification_code}",
                    normal_style,
                ),

                Spacer(
                    1,
                    5,
                ),

                Paragraph(
                    "Scan the QR code to verify "
                    "this transcript online.",
                    normal_style,
                ),
            ],
        ]
    ]

    verification_table = Table(
        verification_data,
        colWidths=[
            45 * mm,
            125 * mm,
        ],
    )

    verification_table.setStyle(
        TableStyle(
            [
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    colors.HexColor("#1f4e79"),
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (0, 0),
                    "CENTER",
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(
        verification_table
    )

    story.append(
        Spacer(
            1,
            25,
        )
    )

    # ==================================================
    # SIGNATURE SECTION
    # ==================================================

    signature_data = [
        [
            "____________________________",
            "____________________________",
        ],

        [
            "Registrar",
            "Dean / Academic Authority",
        ],
    ]

    signature_table = Table(
        signature_data,
        colWidths=[
            85 * mm,
            85 * mm,
        ],
    )

    signature_table.setStyle(
        TableStyle(
            [
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
            ]
        )
    )

    story.append(
        signature_table
    )

    story.append(
        Spacer(
            1,
            20,
        )
    )

    # ==================================================
    # FOOTER
    # ==================================================

    story.append(
        Paragraph(
            "This document was generated by the "
            "WRU Enterprise Management System.",

            ParagraphStyle(
                "Footer",
                parent=normal_style,
                alignment=TA_CENTER,
                fontSize=8,
            ),
        )
    )

    # ==================================================
    # BUILD PDF
    # ==================================================

    document.build(
        story
    )

    buffer.seek(0)

    return buffer