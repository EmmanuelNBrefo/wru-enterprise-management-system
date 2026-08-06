from .models import Transcript


def generate_transcript_report(
    transcript_id
):

    transcript = Transcript.objects.select_related(
        "student"
    ).get(
        id=transcript_id
    )

    summary = transcript.get_transcript_summary()

    return {

        "transcript": transcript,

        "student": summary["student"],

        "academic_records": (
            summary["academic_records"]
        ),

        "cumulative_gpa": (
            summary["cumulative_gpa"]
        ),

    }