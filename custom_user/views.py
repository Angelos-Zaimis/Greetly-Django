import json
from django.http import HttpResponse
from requests import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from custom_user.serializer import UserSerializer, UserInfosSerializer, LanguageSerializerPut, ChangePasswordSerializer, \
    ChangePasswordVerifySerializer
from rest_framework import generics, status
from registration.countries import EU_COUNTRIES, NON_EU_EFTA_COUNTRIES, UK_COUNTRIES
from project import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

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

        refresh = RefreshToken.for_user(user)  # Generate a refresh token for this user

        data = {
            'id': user.id,
            'user': user.email,
            'message': 'Successful login.',
            'username': user.email,
            'tokens': {
                'access':str(refresh.access_token),
                'refresh':str(refresh)
            },
            'first_login': is_first_login,
            'status': user.status,
            'citizenship': user.selectedCitizenship,
            'language': user.language,
            'country': user.country,
            'isSubscribed': user.isSubscribed
        }

        return HttpResponse(json.dumps(data), content_type='application/json', status=200)


    def delete(self, request, *args, **kwargs):
        username = request.data.get('email')
        try:
            user = User.objects.get(email=username)
            user.delete()
            data = {
                'message': 'User deleted successfully.'
            }
            return HttpResponse(json.dumps(data), content_type='application/json', status=200)

        except User.DoesNotExist:
            data = {
                'message': 'User not found.'
            }
            return HttpResponse(json.dumps(data), content_type='application/json', status=404)


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
                'country': user.country,
                'isSubscribed': user.isSubscribed
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
                        citizenship = 'EU-EFTA'
                    elif country.upper() in NON_EU_EFTA_COUNTRIES:
                        citizenship = 'NON-EU-EFTA'
                    elif country.upper() in UK_COUNTRIES:
                        citizenship = 'UK-COUNTRIES'
                user.selectedCitizenship = citizenship

            user.save()
            return HttpResponse(content='Property updated successfully')
        except User.DoesNotExist:
            return HttpResponse(content='User not found', status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        email_body = 'Welcome back ' + user.username.capitalize() + '!' + ' Did you forget your password? No worries \n Copy this code to verify and change your password \n' + 'CODE: ' + str(
            user.code)

        send_mail(
            'Welcome to Greetly.ch',
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False
        )

        return HttpResponse(content='Check your emails, you have received a code to change your password.')


from rest_framework.response import Response

class ChangePasswordVerify(APIView):
    serializer_class = ChangePasswordVerifySerializer

    def patch(self, request, *args, **kwargs):
        print(request)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        email = validated_data.get('email')
        code = validated_data.get('code')
        password = validated_data.get('password')

        try:
            user = User.objects.get(email=email, code=code)
        except User.DoesNotExist:
            return Response({'error': 'User with this email and code combination does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(password)
        user.save()

        return Response({"message": "Password changed successfully."})
