import json

from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        username = request.data.get('email')
        user = User.objects.get(email=username)

        is_first_login = user.first_login

        if is_first_login:
            # Update the user's first_login field in the database
            user.first_login = False
            user.save()

        data = {
            'message': 'Successful login.',
            'username': user.username,
            'token': response.data['access'],
            'first_login': is_first_login
        }
        return HttpResponse(json.dumps(data), content_type='application/json', status=200)