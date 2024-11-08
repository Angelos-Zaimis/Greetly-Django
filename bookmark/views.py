from rest_framework.permissions import IsAuthenticated
from bookmark.serializers import BookmarkSerializer
from bookmark.models import BookMark
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import get_user_model

User = get_user_model()

class BookMarkList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve a list of bookmarks for the specified user."""
        if not request.user.is_authenticated:
            return self.build_unauthenticated_response()

        user = self.get_user_from_request(request)
        if not user:
            return self.build_user_not_found_response()

        bookmarks = BookMark.objects.filter(user=user)
        if not bookmarks.exists():
            return self.build_bookmarks_not_found_response()

        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new bookmark for the specified user."""
        if not request.user.is_authenticated:
            return self.build_unauthenticated_response()

        user = self.get_user_from_request(request)
        if not user:
            return self.build_user_not_found_response()

        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Helper functions
    @staticmethod
    def build_unauthenticated_response():
        """Return response for unauthenticated access."""
        return Response({'detail': 'Authentication credentials were not provided.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def build_user_not_found_response():
        """Return response when a user is not found."""
        return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def build_bookmarks_not_found_response():
        """Return response when no bookmarks are found."""
        return Response({'message': 'Bookmarks not found'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_user_from_request(request):
        """Retrieve a user from the request based on the user email query parameter."""
        user_email = request.query_params.get('user_email')
        if user_email:
            try:
                return User.objects.get(email=user_email.lower())
            except User.DoesNotExist:
                return None
        return None


class BookMarkRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer
    lookup_field = 'uniqueTitle'

    def get_queryset(self):
        """Retrieve the queryset of bookmarks for the given user email."""
        user_email = self.request.query_params.get('user_email')
        user = self.get_user_by_email(user_email)
        if user:
            return BookMark.objects.filter(user=user)
        return BookMark.objects.none()  # Return an empty queryset if user is not found

    def delete(self, request, *args, **kwargs):
        """Delete a bookmark instance."""
        if not request.user.is_authenticated:
            return self.build_unauthenticated_response()

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Helper functions
    @staticmethod
    def get_user_by_email(email):
        """Retrieve a user by their email or return None if not found."""
        if email:
            try:
                return User.objects.get(email=email.lower())
            except User.DoesNotExist:
                return None
        return None

    @staticmethod
    def build_unauthenticated_response():
        """Return response for unauthenticated access."""
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
