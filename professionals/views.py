from rest_framework import generics, status
from rest_framework.response import Response

from professionals.models import Professionals
from professionals.serializers import ProfessionalSerializer


class ProfessionalListView(generics.ListAPIView):
    serializer_class = ProfessionalSerializer

    def get_queryset(self):
        professional_type = self.request.query_params.get('type')

        if professional_type:
            queryset = Professionals.objects.filter(type=professional_type)
            if queryset.exists():
                return queryset
            else:
                return Response({"message": f"Error: No professionals found with type '{professional_type}'."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return  Response({"message": "Error: Professional type not specified."}, status=status.HTTP_404_NOT_FOUND)
