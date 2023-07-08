import json
from django.http import HttpResponse
from requests import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from custom_user.serializer import UserSerializer,UserInfosSerializer,LanguageSerializerPut
import jwt
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin

from registration.countries import EU_COUNTRIES, NON_EU_EFTA_COUNTRIES, UK_COUNTRIES

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('email')
        user = User.objects.get(email=username)
        is_first_login = user.first_login

        if is_first_login:
            # Update the user's first_login field in the database
            user.first_login = False
            user.save()

        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow()
        }
        access_token = jwt.encode(payload, 'SECRET_KEY')

        refresh_payload = {
            'user_id': user.id,
            'email': user.email,
            'type': 'refresh',
            'exp': datetime.utcnow()
        }

        refresh_token = jwt.encode(refresh_payload, 'SECRET_KEY', algorithm='HS256')
        data = {
            'id': user.id,
            'user': user.email,
            'message': 'Successful login.',
            'username': user.email,
            'tokens': {
                'access': access_token,
                'refresh': refresh_token
            },
            'first_login': is_first_login,
            'status': user.status,
            'citizenship': user.selectedCitizenship,
            'language': user.language,
            'country': user.country
        }

        return HttpResponse(json.dumps(data), content_type='application/json', status=200)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'id': user.id,
            'user': user.email,
            'message': 'User updated successfully.',
            'username': user.email,
            # Include any other fields you want to return
            'status': user.status,
            'citizenship': user.selectedCitizenship,
            'language': user.language,
            'country': user.country
        }

        return Response(data, status=status.HTTP_200_OK)

class UserProvider(APIView):
    def get(self, request):
        serializer = UserInfosSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            data = {
                'id': user.id,
                'user': user.email,
                'message': 'User updated successfully.',
                'username': user.email,
                # Include any other fields you want to return
                'status': user.status,
                'citizenship': user.selectedCitizenship,
                'language': user.language,
                'country': user.country
            }
              # Assuming the language is stored in the user's profile model
            return HttpResponse(json.dumps(data))
        except User.DoesNotExist:
            return HttpResponse(status=404, content='User not found')

    def put(self, request):
        serializer = LanguageSerializerPut(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        language = serializer.validated_data.get('language')
        country = serializer.validated_data.get('country')
        status = serializer.validated_data.get('status')

        try:
            user = User.objects.get(email=email)

            if language:
                user.language = language

            if status:
                user.status = status

            if country:
                user.country = country
                if country:
                    if country.upper() in EU_COUNTRIES:
                        citizenship = 'EU/EFTA'
                    elif country.upper() in NON_EU_EFTA_COUNTRIES:
                        citizenship = 'NON-EU/EFTA'
                    elif country.upper() in UK_COUNTRIES:
                        citizenship = 'UK-COUNTRIES'
                user.selectedCitizenship = citizenship

            user.save()
            return HttpResponse(content='Property updated successfully')
        except User.DoesNotExist:
            return HttpResponse(content='User not found', status=status.HTTP_404_NOT_FOUND)
