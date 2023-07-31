import socket
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import re

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

    if value.endswith('@example.com'):
        raise ValidationError('Email address is a known disposable address')
    if value.endswith('@spamdomain.com'):
        raise ValidationError('Email address is a known spam address')


def custom_password_validator(value):
    """
    Check that the password meets custom requirements.
    """
    # Example custom password validation rules
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not any(char.isdigit() for char in value):
        raise ValidationError('Password must contain at least one digit.')
    if not any(char.isupper() for char in value):
        raise ValidationError('Password must contain at least one uppercase letter.')
    if not any(char.islower() for char in value):
        raise ValidationError('Password must contain at least one lowercase letter.')
    # Add more custom password validation rules as needed


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[custom_email_validator])
    password = serializers.CharField(validators=[validate_password, custom_password_validator])

    class Meta:
        model = User
        fields = ['email', 'password', 'status', 'selectedCitizenship','country' ]

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Authenticate the user with the provided credentials
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password')

        # Add the authenticated user to the validated data dictionary
        data['user'] = user
        return data


class UserInfosSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = '__all__'


class LanguageSerializerPut(serializers.Serializer):
    email = serializers.EmailField(required=True)
    language = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")
        return value

class ChangePasswordVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    code = serializers.CharField(max_length=555, required=True)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        try:
            user = User.objects.get(email=email, code=code)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with given email and code does not exist.")

        return data