from socket import socket
from typing import re

from botocore.exceptions import ValidationError
from django.core.validators import EmailValidator
from rest_framework import serializers
from registration.models import Registration
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth import get_user_model

User = get_user_model()



def custom_email_validator(value):
    # Check for valid format
    try:
        EmailValidator()(value)
    except ValidationError:
        raise ValidationError('Invalid email format')

    # Check for invalid characters
    if re.search(r'[^\w.@+-]', value):
        raise ValidationError('Email contains invalid characters')

    # Check for missing username or domain
    if not re.match(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', value):
        raise ValidationError('Email is missing username or domain')

    # Check for valid domain
    domain = value.split('@')[1]
    try:
        _, _, addresses = socket.gethostbyname_ex(domain)
        if not addresses:
            raise ValidationError('Email domain does not exist')
    except (socket.herror, socket.gaierror):
        raise ValidationError('Email domain does not exist')

    # Check for valid TLD
    tld = domain.split('.')[-1]
    if not re.match(r'[a-zA-Z]{2,}', tld):
        raise ValidationError('Invalid email top-level domain')

    # Check for email length
    if len(value) > 254:
        raise ValidationError('Email address is too long')

    # Check if email already exists
    if User.objects.filter(email=value).exists():
        raise ValidationError('Email address already exists')

    # Check if email is disposable or spam
    # (This is just an example, you would need to use a third-party service or database to check for these)
    if value.endswith('@example.com'):
        raise ValidationError('Email address is a known disposable address')
    if value.endswith('@spamdomain.com'):
        raise ValidationError('Email address is a known spam address')

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(validators=[
        MinLengthValidator(7, message="Password must be at least 8 characters"),
        MaxLengthValidator(20, message="Password cannot be more than 20 numbers")
    ],
    write_only=True,
    style={'input_type': 'password'})
    email = serializers.EmailField(validators=[custom_email_validator])
    selectedCitizenship = serializers.CharField(required=True)
    status = serializers.CharField(required=True)

    class Meta:
        model = Registration
        fields = ['email','password','selectedCitizenship','status']


    def create(self, validated_data):
        # Create a new user instance with the email and password
        user = User.objects.create_user(username=validated_data['email'],email=validated_data['email'], password=validated_data['password'])
        # Create a new registration instance with the user and verification code
        registration = Registration.objects.create(user=user)
        return registration



class VerifyRegistrationSerializer(serializers.Serializer):
    verification_code = serializers.IntegerField(required=True)


    class Meta:
        model =Registration
        fields = ['verification_code']