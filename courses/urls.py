from django.urls import path
from .views import course_list, course_detail

urlpatterns = [
    path("", course_list, name="course-list"),
    path("<int:pk>/", course_detail, name="course-detail"),
]