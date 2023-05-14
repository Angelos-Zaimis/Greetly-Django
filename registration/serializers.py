import re
import socket

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from rest_framework import serializers

from registration.countries import NON_EU_EFTA_COUNTRIES, EU_COUNTRIES,UK_COUNTRIES
from registration.languages import COUNTRY_LANGUAGES
from registration.models import Registration

User = get_user_model()


def get_language(country):
    for item in COUNTRY_LANGUAGES:
        if item['country'] == country:
            return item['language']
    return 'English'

def custom_email_validator(value):

    try:
        EmailValidator()(value)
    except ValidationError:
        raise ValidationError('')

    if re.search(r'[^\w.@+-]', value):
        raise ValidationError('Email contains invalid characters')

    if not re.match(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', value):
        raise ValidationError('Email is missing username or domain')

    domain = value.split('@')[1]
    try:
        _, _, addresses = socket.gethostbyname_ex(domain)
        if not addresses:
            raise ValidationError('Email domain does not exist')
    except (socket.herror, socket.gaierror):
        raise ValidationError('Email domain does not exist')

    tld = domain.split('.')[-1]
    if not re.match(r'[a-zA-Z]{2,}', tld):
        raise ValidationError('Invalid email top-level domain')

    if len(value) > 254:
        raise ValidationError('Email address is too long')

    if User.objects.filter(email=value).exists():
        raise ValidationError('Email address already exists')

    if value.endswith('@example.com'):
        raise ValidationError('Email address is a known disposable address')
    if value.endswith('@spamdomain.com'):
        raise ValidationError('Email address is a known spam address')


def custom_password_validator(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not any(char.isdigit() for char in value):
        raise ValidationError('Password must contain at least one digit.')
    if not any(char.isupper() for char in value):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not any(char.islower() for char in value):
        raise ValidationError('Password must contain at least one lowercase letter.')
    if not any(char in "!@#$%^&*()_+-=[]{};:,.<>/?`~" for char in value):
        raise ValidationError('Password must contain at least one special character.')





class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(validators=[custom_email_validator])
    password = serializers.CharField(validators=[custom_password_validator])
    selectedCountry = serializers.CharField(required=True)
    status = serializers.CharField(required=True)

    class Meta:
        model = Registration
        fields = ['email','password','selectedCountry','status']


    def create(self, validated_data):


        country = validated_data.get('selectedCountry')

        citizenship = None

        if country:
            if country.upper() in EU_COUNTRIES:
                citizenship = 'EU/EFTA'
            elif country.upper() in NON_EU_EFTA_COUNTRIES:
                citizenship = 'NON-EU/EFTA'
            elif country.upper() in UK_COUNTRIES:
                citizenship = 'UK-COUNTRIES'
            else:
                raise serializers.ValidationError('Invalid country')




        user = User.objects.create_user(username=validated_data['email'],
                                        email=validated_data['email'],
                                        password=validated_data['password'],
                                        status=validated_data['status'],
                                        selectedCitizenship=citizenship,
                                        language=get_language(country)
                                        )
        # Create a new registration instance with the user and verification code
        registration = Registration.objects.create(user=user)
        return registration


class VerifyRegistrationSerializer(serializers.Serializer):
    verification_code = serializers.IntegerField(required=True)


    class Meta:
        model =Registration
        fields = ['verification_code']