from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializers import (
    StudentSerializer,
    StudentCreateSerializer,
)


# ===========================================
# LIST & CREATE
# ===========================================
@api_view(["GET", "POST"])
def student_list(request):

    if request.method == "GET":
        students = Student.objects.all()
        serializer = StudentSerializer(
            students,
            many=True
        )
        return Response(serializer.data)

    serializer = StudentCreateSerializer(
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


# ===========================================
# RETRIEVE / UPDATE / DELETE
# ===========================================
@api_view(["GET", "PUT", "DELETE"])
def student_detail(request, student_id):

    try:
        student = Student.objects.get(
            student_id=student_id
        )
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # --------------------
    # GET ONE
    # --------------------
    if request.method == "GET":
        serializer = StudentCreateSerializer(student)
        return Response(serializer.data)

    # --------------------
    # UPDATE
    # --------------------
    if request.method == "PUT":
        serializer = StudentCreateSerializer(
            student,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------
    # DELETE
    # --------------------
    student.delete()

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )