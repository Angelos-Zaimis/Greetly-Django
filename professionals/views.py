from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Professionals
from .serializers import ProfessionalSerializer

class ProfessionalListView(generics.ListAPIView):
    serializer_class = ProfessionalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the queryset based on professional type and canton."""
        professional_type, canton = self.get_query_params()
        self.validate_query_params(professional_type, canton)
        return self.filter_professionals(professional_type, canton)

    def list(self, request, *args, **kwargs):
        """Return a list of professionals based on query parameters."""
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except ValidationError as e:
            return self.build_error_response(str(e), status.HTTP_400_BAD_REQUEST)

        if not queryset.exists():
            self.handle_no_results_found()

        return self.build_response(queryset)

    # Helper functions
    def get_query_params(self):
        """Extract and return type and canton from query parameters."""
        return (
            self.request.query_params.get('type'),
            self.request.query_params.get('canton')
        )

    @staticmethod
    def validate_query_params(professional_type, canton):
        """Validate that both type and canton are provided."""
        if not professional_type or not canton:
            raise ValidationError("Professional type and canton must be specified.")

    @staticmethod
    def filter_professionals(professional_type, canton):
        """Filter professionals based on type and canton."""
        return Professionals.objects.filter(type=professional_type, canton=canton)

    def handle_no_results_found(self):
        """Handle cases where no professionals are found."""
        professional_type = self.request.query_params.get('type')
        canton = self.request.query_params.get('canton')
        raise Http404(f"No professionals found with type '{professional_type}' in canton '{canton}'.")

    @staticmethod
    def build_error_response(message, status_code):
        """Build an error response with a given message and status code."""
        return Response({"detail": message}, status=status_code)

    def build_response(self, queryset):
        """Build and return the response for the given queryset."""
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)