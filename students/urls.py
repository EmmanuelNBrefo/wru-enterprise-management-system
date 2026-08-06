from django.urls import path
from .views import student_list, student_detail

urlpatterns = [
    path("", student_list, name="student-list"),

    path(
        "<str:student_id>/",
        student_detail,
        name="student-detail",
    ),
]