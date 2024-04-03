from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Professionals  # Adjust the import according to your app structure
from .serializers import ProfessionalSerializer  # Adjust the import according to your app structure


class ProfessionalListView(generics.ListAPIView):
    serializer_class = ProfessionalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        professional_type = self.request.query_params.get('type')
        canton = self.request.query_params.get('canton')

        if not professional_type or not canton:
            # Using ValidationError to indicate bad request data
            raise ValidationError("Professional type and canton must be specified.")

        queryset = Professionals.objects.filter(type=professional_type, canton=canton)
        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except ValidationError as e:
            # Return a 400 Bad Request response if there is a validation error
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not queryset.exists():
            # Raising Http404 will be caught by DRF and return a 404 Not Found response
            raise Http404(
                f"No professionals found with type '{request.query_params.get('type')}' in canton '{request.query_params.get('canton')}'.")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
