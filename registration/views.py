import json

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .models import Registration
from project import settings
from registration.serializers import RegisterSerializer, VerifyRegistrationSerializer


# Create your views here.



class RegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            errors = json.dumps(e.detail)
            return HttpResponse(errors, status=status.HTTP_400_BAD_REQUEST)

        registration = serializer.save()

        email_body = f"Welcome to HelloCH {registration.user.username.capitalize()}! \n" \
                     f"Verify your email by copying the verification code below:\n\n" \
                     f"CODE: {registration.verification_code}"

        send_mail(
            'Welcome to HelloCh',
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [registration.user.email],
            fail_silently=False
        )

        data = {'message': 'Check your email to verify your account'}
        return HttpResponse(data, status=status.HTTP_201_CREATED)

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
