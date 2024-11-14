from rest_framework import serializers, status
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from rest_framework.response import Response

from custom_user.countries import EU_COUNTRIES, NON_EU_EFTA_COUNTRIES, UK_COUNTRIES
from custom_user.languages import COUNTRY_LANGUAGES
from custom_user.validators import custom_email_validator, custom_password_validator

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[custom_email_validator])
    password = serializers.CharField(validators=[validate_password, custom_password_validator])

    class Meta:
        model = User
        fields = ['email', 'password', 'status', 'selectedCitizenship', 'country']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email.lower(), password=password)
        if not user:
            raise serializers.ValidationError({'message': 'Invalid email or password.'})

        data['user'] = user
        return data


class UserInfosSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(required=True)

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

    @staticmethod
    def validate_email(value):
        try:
            User.objects.get(email=value.lower())
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return value


class ChangePasswordVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    code = serializers.CharField(max_length=555, required=True)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        try:
            user = User.objects.get(email=email.lower(), code=code)
        except User.DoesNotExist:
            raise ValidationError({'message': 'User with this email does not exist or code is wrong'})
        return data


class UserExistsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']


def get_language(country):
    for item in COUNTRY_LANGUAGES:
        if item['country'] == country:
            return item['language']
    return 'English'


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[custom_email_validator])
    password = serializers.CharField(validators=[custom_password_validator])
    country = serializers.CharField(required=True)
    status = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'country', 'status']

    def create(self, validated_data):
        """Create a new user and set citizenship based on the selected country."""
        country = validated_data.get('country')
        citizenship = self.determine_citizenship(country)

        user = self.create_user(validated_data, country, citizenship)
        return user

    @staticmethod
    def determine_citizenship(country):
        """Determine the citizenship based on the selected country."""
        if not country:
            raise serializers.ValidationError('Country must be provided')

        country_upper = country.upper()
        if country_upper in EU_COUNTRIES:
            return 'EU-EFTA'
        elif country_upper in NON_EU_EFTA_COUNTRIES:
            return 'NON-EU-EFTA'
        elif country_upper in UK_COUNTRIES:
            return 'UK-COUNTRIES'
        else:
            raise serializers.ValidationError('Invalid country')

    @staticmethod
    def create_user(validated_data, country, citizenship):
        """Create a user instance with the provided validated data."""
        return User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'].lower(),
            password=validated_data['password'],
            status=validated_data['status'],
            selectedCitizenship=citizenship,
            country=country,
            language=get_language(country),
            is_active=True
        )


class VerifyRegistrationSerializer(serializers.Serializer):
    verification_code = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['verification_code']
