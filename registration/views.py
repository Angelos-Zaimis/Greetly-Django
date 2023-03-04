from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from requests import Response
from rest_framework import generics

from project import settings
from registration.serializers import RegisterSerializer

# Create your views here.



class RegistrationView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        user = request.data #we get the data of the user
        serializer = self.serializer_class(data=user) # pass user to serializer to validate data
        serializer.is_valid(raise_exception=True) #serializer validation
        registration = serializer.save() #if data is correct -save

        email_body = f"Welcome to EasyMove {registration.user.username.capitalize()}! \n" \
                     f"Verify your email by copying the verification code below:\n\n" \
                     f"CODE: {registration.verification_code}"

        send_mail(
            'Welcome to EasyMove',
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [registration.user.email],
            fail_silently=False
        )

        data = {'message: Check your email to verify you account'}

        return HttpResponse(data)
