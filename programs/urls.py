from django.urls import path
from .views import program_list

urlpatterns = [
    path(
        "",
        program_list,
        name="program-list",
    ),
]