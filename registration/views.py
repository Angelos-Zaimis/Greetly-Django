from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from .models import Registration
from project import settings
from registration.serializers import RegisterSerializer, VerifyRegistrationSerializer

from rest_framework.exceptions import ValidationError
# Create your views here.


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        registration = serializer.save()

        email_body = f"Welcome to Hello.CH {registration.user.email}! \n" \
                     f"Verify your email by copying the verification code below:\n\n" \
                     f"CODE: {registration.verification_code}"

        send_mail(
            'Welcome to Hello.CH',
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [registration.user.email],
            fail_silently=False
        )

        data = {'Check your email to verify your account!!!'}
        return HttpResponse(data)

class VerifyRegistrationView(APIView):
    serializer_class = VerifyRegistrationSerializer

    def put(self, request):
        code = request.data.get('verification_code')
        try:
            registration = Registration.objects.get(verification_code=code)
        except Registration.DoesNotExist:
            return HttpResponse({'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)

        user = registration.user
        if not user.is_verified:
            user.is_verified = True
            user.save()

        registration.status = 'active'
        registration.save()

        return HttpResponse({'Registration successful!'}, status=status.HTTP_200_OK)
