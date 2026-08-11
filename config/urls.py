from django.contrib import admin
from django.urls import include, path

import config.admin


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "transcripts/",
        include("transcripts.urls")
    ),

    path(
        "api/students/",
        include("students.urls")
    ),

    path(
        "api/programs/",
        include("programs.urls")
    ),

    path(
        "api/admissions/",
        include("admissions.urls")
    ),
    path(
    "api/registrations/",
    include("registrations.urls"),
),

]