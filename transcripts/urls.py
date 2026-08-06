from django.urls import path

from .views import (
    transcript_detail,
    transcript_pdf,
    verify_transcript,
)


app_name = "transcripts"


urlpatterns = [

    path(

        "",

        verify_transcript,

        name="verify_home"

    ),

    path(

        "verify/<str:verification_code>/",

        verify_transcript,

        name="verify"

    ),

    path(

        "<int:transcript_id>/",

        transcript_detail,

        name="detail"

    ),

    path(

        "<int:transcript_id>/pdf/",

        transcript_pdf,

        name="pdf"

    ),

]