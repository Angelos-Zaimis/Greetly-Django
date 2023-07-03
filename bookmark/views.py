from django.shortcuts import render
from bookmark.serializers import BookmakrkSerializer, BookmakrkCreateSerializer
from bookmark.models import BookMark
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.


class BookMarkList(APIView):
    def get(self, request):
        user_email = request.query_params.get('user_email')
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        bookmarks = BookMark.objects.filter(user=user)
        serializer = BookmakrkSerializer(bookmarks, many=True)
        return Response(serializer.data)


    def post(self, request):
        user_email = request.query_params.get('user_email')
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookmakrkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class BookMarkRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookmakrkSerializer
    lookup_field = 'uniqueTitle'

    def get_queryset(self):
        user_email = self.request.query_params.get('user_email')
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return BookMark.objects.none()

        return BookMark.objects.filter(user=user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)