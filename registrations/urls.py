from django.urls import path

from .views import (
    registration_list,
    registration_detail,
)


urlpatterns = [

    path(
        "",
        registration_list,
        name="registration-list"
    ),

    path(
        "<str:registration_no>/",
        registration_detail,
        name="registration-detail"
    ),

]