from requests import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from custom_user.serializer import UserSerializer, UserInfosSerializer, LanguageSerializerPut, ChangePasswordSerializer, \
    ChangePasswordVerifySerializer, UserExistsSerializer
from rest_framework import generics, status
from registration.countries import EU_COUNTRIES, NON_EU_EFTA_COUNTRIES, UK_COUNTRIES
from project import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
import random
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


def generate_code(length=5):
    random.seed(time.time())  # Seed based on the current time
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for _ in range(length))


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('email')
        user = User.objects.get(email__iexact=username)
        is_first_login = user.first_login

        if is_first_login:
            user.first_login = False
            user.save()

        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)

        data = {
            'id': user.id,
            'user': user.email,
            'message': 'Successful login.',
            'username': user.email,
            'tokens': {
                'access': str(access),
                'refresh': str(refresh)
            },
            'first_login': is_first_login,
            'status': user.status,
            'citizenship': user.selectedCitizenship,
            'language': user.language,
            'country': user.country,
            'isSubscribed': user.isSubscribed,
            'product_details': {
                'subscription_plan': user.product_details.get('subscription_plan', ''),
                'subscription_price': user.product_details.get('subscription_price', ''),
                'subscription_currency': user.product_details.get('subscription_currency', ''),
                'subscription_id': user.product_details.get('subscription_id', '')

            }
        }

        return Response(data, content_type='application/json', status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        username = request.data.get('email')
        try:
            user = User.objects.get(email__iexact=username)

            user.delete()
            data = {
                'message': 'User deleted successfully.'
            }
            return Response(data, content_type='application/json', status=status.HTTP_200_OK)

        except User.DoesNotExist:
            data = {
                'message': 'User not found.'
            }
            return Response(data, content_type='application/json', status=status.HTTP_404_NOT_FOUND)

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
            'status': user.status,
            'citizenship': user.selectedCitizenship,
            'language': user.language,
            'country': user.country
        }

        return Response(data, status=status.HTTP_200_OK)


class UserProvider(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserInfosSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email__iexact=email)
            data = {
                'id': user.id,
                'user': user.email,
                'message': 'User updated successfully.',
                'username': user.email,
                'status': user.status,
                'citizenship': user.selectedCitizenship,
                'language': user.language,
                'country': user.country,
                'isSubscribed': user.isSubscribed,
                'product_details': {
                    'subscription_plan': user.product_details.get('subscription_plan', ''),
                    'subscription_price': user.product_details.get('subscription_price', ''),
                    'subscription_currency': user.product_details.get('subscription_currency', ''),
                    'subscription_id': user.product_details.get('subscription_id', '')
                }
            }
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Users info not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = LanguageSerializerPut(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        language = serializer.validated_data.get('language')
        country = serializer.validated_data.get('country')
        user_status = serializer.validated_data.get('status')

        try:
            user = User.objects.get(email=email)

            if language:
                user.language = language

            if user_status:
                user.status = user_status

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
            return Response({"message": "Property updated successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_email = serializer.validated_data['email']
        try:
            user = User.objects.get(email__iexact=user_email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user.code = generate_code()
        user.save()
        email_body = 'Welcome back ' + user.username.capitalize() + '!' + '\n' + 'Did you forget your password?\nNo ' \
                                                                                 'worries ' \
                                                                                 '\nCopy this code to verify and ' \
                                                                                 'change ' \
                                                                                 'your password \n' + 'CODE: ' + str(
            user.code)

        send_mail(
            'Welcome to Greetly.ch',
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False
        )

        return Response({"message": "Check your emails, you have received a code to change your password"})


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
            user = User.objects.get(email__iexact=email, code=code)
        except User.DoesNotExist:
            return Response({'message': 'User with this email and code combination does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        user.set_password(password)
        user.save()

        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)


class UserGoogleExists(TokenObtainPairView):
    serializer_class = UserExistsSerializer

    def post(self, request, *args, **kwargs):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)

        username = user_data.get('email')

        try:
            user = User.objects.get(email__iexact=username)
            return Response({"message": f"{user} exists in the database"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User doesn't exist in the database"}, status=status.HTTP_404_NOT_FOUND)


class GoogleLoginView(APIView):
    def post(self, request):
        google_token = request.data.get('googleToken')
        if not google_token:
            return Response({'error': 'Google token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(google_token, requests.Request())
            # Here, you can validate idinfo and extract user data
            # You may want to check if the user exists in your database and create one if needed

            # Check if the user exists in the database based on email
            user = User.objects.get(email=idinfo['email'])

            # Generate JWT token

            access = AccessToken.for_user(user)
            refresh = RefreshToken.for_user(user)
            return Response({'accessToken': str(access), 'refreshToken': str(refresh)},
                            status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)
