from django.urls import path

from .views import (
    admission_list,
    admission_detail,
)


urlpatterns = [

    path(
        "",
        admission_list,
        name="admission-list"
    ),

    path(
        "<str:admission_no>/",
        admission_detail,
        name="admission-detail"
    ),

]