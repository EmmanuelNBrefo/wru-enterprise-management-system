from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Program
from .serializers import ProgramSerializer


@api_view(["GET"])
def program_list(request):
    """
    Return all active academic programs.
    """

    programs = Program.objects.filter(
        is_active=True
    ).order_by("name")

    serializer = ProgramSerializer(
        programs,
        many=True
    )

    return Response(serializer.data)