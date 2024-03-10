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
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        user_email = request.query_params.get('user_email')

        try:
            user = User.objects.get(email=user_email.lower())
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        bookmarks = BookMark.objects.filter(user=user)

        if len(bookmarks) == 0:
            return Response({'message': 'Bookmarks not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        user_email = request.query_params.get('user_email')
        try:
            user = User.objects.get(email=user_email.lower())
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookMarkRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer
    lookup_field = 'uniqueTitle'

    def get_queryset(self):
        user_email = self.request.query_params.get('user_email')
        try:
            user = User.objects.get(email=user_email.lower())
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        return BookMark.objects.filter(user=user)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
