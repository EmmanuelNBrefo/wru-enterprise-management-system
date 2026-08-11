from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Registration
from .serializers import RegistrationSerializer


# ==========================================
# LIST & CREATE REGISTRATIONS
# ==========================================

@api_view(["GET", "POST"])
def registration_list(request):

    # ----------------------------
    # GET ALL REGISTRATIONS
    # ----------------------------

    if request.method == "GET":

        registrations = Registration.objects.select_related(
            "student",
            "student__program"
        ).all()

        serializer = RegistrationSerializer(
            registrations,
            many=True
        )

        return Response(serializer.data)

    # ----------------------------
    # CREATE REGISTRATION
    # ----------------------------

    serializer = RegistrationSerializer(
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# ==========================================
# RETRIEVE / UPDATE / DELETE
# ==========================================

@api_view(["GET", "PUT", "DELETE"])
def registration_detail(
    request,
    registration_no
):

    # ----------------------------
    # FIND REGISTRATION
    # ----------------------------

    try:

        registration = Registration.objects.select_related(
            "student",
            "student__program"
        ).get(
            registration_no=registration_no
        )

    except Registration.DoesNotExist:

        return Response(
            {
                "error": "Registration not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # ----------------------------
    # GET ONE
    # ----------------------------

    if request.method == "GET":

        serializer = RegistrationSerializer(
            registration
        )

        return Response(
            serializer.data
        )

    # ----------------------------
    # UPDATE
    # ----------------------------

    if request.method == "PUT":

        serializer = RegistrationSerializer(
            registration,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # ----------------------------
    # DELETE
    # ----------------------------

    registration.delete()

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )