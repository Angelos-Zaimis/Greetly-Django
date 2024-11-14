import random
import time
from venv import logger

from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from google.auth.transport import requests
from google.oauth2 import id_token
from requests import Response
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from custom_user.serializer import UserInfosSerializer, LanguageSerializerPut, ChangePasswordSerializer, \
    ChangePasswordVerifySerializer, UserExistsSerializer, RegisterSerializer
from project import settings
from custom_user.countries import EU_COUNTRIES, NON_EU_EFTA_COUNTRIES, UK_COUNTRIES
from django.template.loader import render_to_string
User = get_user_model()

def generate_code(length=5):
    random.seed(time.time())
    numbers = '0123456789'
    return ''.join(random.choice(numbers) for _ in range(length))

class UserProvider(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_id = self.validate_and_get_id(UserInfosSerializer, request.query_params)
            if not user_id:
                logger.error("Invalid or missing user_id in query params")
                return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Exception during ID validation: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_user_by_id(user_id)
        if not user:
            logger.error(f"No user found for ID: {user_id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        response_data = self.build_user_response_data(user)
        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request):
        validated_data = self.validate_and_get_data(LanguageSerializerPut, request.data)
        email = validated_data['email']
        user = self.get_user_by_email(email)

        self.update_user_properties(user, validated_data)
        return Response({"message": "Property updated successfully"}, status=status.HTTP_200_OK)

    @staticmethod
    def get_user_by_email(email):
        """Retrieve a user by email, raising a 404 if not found."""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def validate_and_get_id(serializer_class, data):
        """Validate and return the email from the serializer."""
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data['user_id']

    @staticmethod
    def validate_and_get_data(serializer_class, data):
        """Validate and return the validated data from the serializer."""
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @staticmethod
    def get_user_by_id(user_id):
        """Retrieve a user by email, raising a 404 if not found."""
        return get_object_or_404(User, id=user_id)

    @staticmethod
    def build_user_response_data(user):
        """Build response data for the get method."""
        return {
            'id': user.id,
            'user': user.email,
            'message': 'User updated successfully.',
            'username': user.email,
            'status': user.status,
            'citizenship': user.selectedCitizenship,
            'language': user.language,
            'country': user.country,
        }

    @staticmethod
    def update_user_properties(user, data):
        """Update user properties based on the provided data."""
        language = data.get('language')
        user_status = data.get('status')
        country = data.get('country')

        if language:
            user.language = language

        if user_status:
            user.status = user_status

        if country:
            user.country = country
            user.selectedCitizenship = UserProvider.determine_citizenship(country)

        user.save()

    @staticmethod
    def determine_citizenship(country):
        """Determine citizenship based on the country."""
        if country.upper() in EU_COUNTRIES:
            return 'EU-EFTA'
        elif country.upper() in NON_EU_EFTA_COUNTRIES:
            return 'NON-EU-EFTA'
        elif country.upper() in UK_COUNTRIES:
            return 'UK-COUNTRIES'
        return None

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        """Handle password change request by sending a verification code to the user's email."""
        serializer = self.validate_serializer(request.data)
        user = self.get_user_by_email(serializer.validated_data['email'])

        user.code = self.generate_and_save_user_code(user)
        self.send_verification_email(user)

        return Response(
            {"message": "Check your emails, you have received a code to change your password"},
            status=status.HTTP_200_OK
        )

    # Helper functions
    def validate_serializer(self, data):
        """Validate the provided serializer data."""
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer

    @staticmethod
    def get_user_by_email(email):
        """Retrieve a user by email, raising a 404 if not found."""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def generate_and_save_user_code(user):
        """Generate a new code for the user and save it."""
        user.code = generate_code()
        user.save()
        return user.code

    @staticmethod
    def send_verification_email(user):
        """Send a verification email to the user with the generated code."""
        email_body = (
            f'Welcome back {user.username.capitalize()}!\n'
            'Did you forget your password?\n'
            'No worries.\n'
            'Copy this code to verify and change your password:\n'
            f'CODE: {user.code}'
        )
        send_mail(
            'Welcome to Greetly.ch',
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )

class ChangePasswordVerify(APIView):
    serializer_class = ChangePasswordVerifySerializer

    def patch(self, request, *args, **kwargs):
        """Verify code and change password for the user."""
        serializer = self.validate_serializer(request.data)
        validated_data = serializer.validated_data

        user = self.get_user_by_email_and_code(
            email=validated_data.get('email'),
            code=validated_data.get('code')
        )

        self.change_user_password(user, validated_data.get('password'))

        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

    # Helper functions
    def validate_serializer(self, data):
        """Validate the provided serializer data."""
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer

    @staticmethod
    def get_user_by_email_and_code(email, code):
        """Retrieve user by email and code, raising a 404 if not found."""
        try:
            return User.objects.get(email=email.lower(), code=code)
        except User.DoesNotExist:
            raise Response(
                {'message': 'User with this email and code combination does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

    @staticmethod
    def change_user_password(user, password):
        """Set a new password for the user and save it."""
        user.set_password(password)
        user.save()


class UserGoogleExists(TokenObtainPairView):
    serializer_class = UserExistsSerializer

    def post(self, request, *args, **kwargs):
        """Check if a user with the given email exists in the database."""
        user_data = request.data
        serializer = self.validate_serializer(user_data)
        email = serializer.validated_data['email'].lower()

        if self.check_user_exists(email):
            return Response({"message": f"User with email {email} exists in the database"}, status=status.HTTP_200_OK)
        return Response({"message": "User doesn't exist in the database"}, status=status.HTTP_404_NOT_FOUND)

    # Helper functions
    def validate_serializer(self, data):
        """Validate the provided serializer data."""
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer

    @staticmethod
    def check_user_exists(email):
        """Check if a user with the given email exists."""
        return User.objects.filter(email=email).exists()

class GoogleLoginView(APIView):
    def post(self, request):
        """Handle user login using Google token."""
        google_token = request.data.get('googleToken')
        if not google_token:
            return self.build_error_response('Google token is required', status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = self.verify_google_token(google_token)
            user = self.get_or_create_user(idinfo)

            tokens = self.generate_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        except ValueError:
            return self.build_error_response('Invalid Google token', status.HTTP_400_BAD_REQUEST)

    # Helper functions
    @staticmethod
    def build_error_response(message, status_code):
        """Build a standardized error response."""
        return Response({'error': message}, status=status_code)

    @staticmethod
    def verify_google_token(google_token):
        """Verify the Google OAuth2 token and return user info."""
        return id_token.verify_oauth2_token(google_token, requests.Request())

    @staticmethod
    def get_or_create_user(idinfo):
        """Retrieve or create a user based on the email from Google token info."""
        email = idinfo['email'].lower()
        user, created = User.objects.get_or_create(email=email, defaults={
            'username': idinfo.get('name', email),
            # Add any additional default user properties if necessary
        })
        return user

    @staticmethod
    def generate_tokens_for_user(user):
        """Generate access and refresh tokens for the user."""
        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)
        return {
            'accessToken': str(access),
            'refreshToken': str(refresh),
        }

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.notify_user_registered(user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def notify_user_registered(user_email):
        subject = "Welcome to Greetly.ch"

        html_content = render_to_string('user_registration_notification.html', {
            'email': user_email,
        })

        email = EmailMessage(
            subject,
            html_content,
            settings.DEFAULT_FROM_EMAIL,
            [user_email]
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)