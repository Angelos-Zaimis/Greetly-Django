import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


def custom_email_validator(value):
    try:
        EmailValidator()(value)
    except ValidationError:
        raise ValidationError('Invalid email format')

    if re.search(r'[^\w.@+-]', value):
        raise ValidationError('Email contains invalid characters')

    if not re.match(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', value):
        raise ValidationError('Email is missing username or domain')

    if len(value) > 254:
        raise ValidationError('Email address is too long')

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
