from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Admission
from .serializers import AdmissionSerializer


@api_view(["GET", "POST"])
def admission_list(request):

    if request.method == "GET":

        admissions = Admission.objects.select_related(
            "student"
        ).all()

        serializer = AdmissionSerializer(
            admissions,
            many=True
        )

        return Response(serializer.data)

    serializer = AdmissionSerializer(
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


@api_view(["GET", "PUT", "DELETE"])
def admission_detail(
    request,
    admission_no
):

    try:

        admission = Admission.objects.select_related(
            "student"
        ).get(
            admission_no=admission_no
        )

    except Admission.DoesNotExist:

        return Response(
            {"error": "Admission not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":

        serializer = AdmissionSerializer(
            admission
        )

        return Response(serializer.data)

    if request.method == "PUT":

        serializer = AdmissionSerializer(
            admission,
            data=request.data,
            partial=True
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

    admission.delete()

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )