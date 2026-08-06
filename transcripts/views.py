from django.http import FileResponse
from django.shortcuts import render

from .models import Transcript
from .pdf_service import generate_transcript_pdf
from .services import generate_transcript_report


def transcript_detail(
    request,
    transcript_id
):

    report = generate_transcript_report(
        transcript_id
    )

    return render(

        request,

        "transcripts/transcript_detail.html",

        {

            "report": report

        }

    )


def transcript_pdf(
    request,
    transcript_id
):

    pdf_buffer = generate_transcript_pdf(

        transcript_id

    )

    transcript = Transcript.objects.get(

        id=transcript_id

    )

    filename = (

        f"transcript_"

        f"{transcript.student.student_id}"

        f".pdf"

    )

    return FileResponse(

        pdf_buffer,

        as_attachment=True,

        filename=filename

    )


def verify_transcript(

    request,

    verification_code=None

):

    # -----------------------------------------
    # GET VERIFICATION CODE
    # -----------------------------------------

    if not verification_code:

        verification_code = request.GET.get(

            "verification_code",

            ""

        ).strip()

    # -----------------------------------------
    # INITIAL VALUES
    # -----------------------------------------

    transcript = None

    summary = None

    valid = False

    verification_status = (

        "NOT_FOUND"

    )

    # -----------------------------------------
    # SEARCH FOR TRANSCRIPT
    # -----------------------------------------

    if verification_code:

        transcript = (

            Transcript.objects

            .filter(

                verification_code=

                verification_code

            )

            .select_related(

                "student"

            )

            .first()

        )

    # -----------------------------------------
    # CHECK TRANSCRIPT STATUS
    # -----------------------------------------

    if transcript:

        summary = (

            transcript

            .get_transcript_summary()

        )

        # -------------------------------------
        # ACTIVE AND OFFICIAL
        # -------------------------------------

        if (

            transcript.status

            == Transcript.STATUS_ACTIVE

            and transcript.is_official

        ):

            valid = True

            verification_status = (

                "VALID"

            )

        # -------------------------------------
        # REVOKED
        # -------------------------------------

        elif (

            transcript.status

            == Transcript.STATUS_REVOKED

        ):

            verification_status = (

                "REVOKED"

            )

        # -------------------------------------
        # EXPIRED
        # -------------------------------------

        elif (

            transcript.status

            == Transcript.STATUS_EXPIRED

        ):

            verification_status = (

                "EXPIRED"

            )

        # -------------------------------------
        # PENDING
        # -------------------------------------

        elif (

            transcript.status

            == Transcript.STATUS_PENDING

        ):

            verification_status = (

                "PENDING"

            )

        # -------------------------------------
        # OTHER INVALID CASE
        # -------------------------------------

        else:

            verification_status = (

                "INVALID"

            )

    # -----------------------------------------
    # DISPLAY VERIFICATION PAGE
    # -----------------------------------------

    return render(

        request,

        "transcripts/verify_transcript.html",

        {

            "transcript": transcript,

            "student": (

                transcript.student

                if transcript

                else None

            ),

            "summary": summary,

            "verification_code": (

                verification_code

            ),

            "valid": valid,

            "verification_status": (

                verification_status

            ),

        }

    )