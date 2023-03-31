from django.core.validators import EmailValidator
from rest_framework import serializers
from registration.models import Registration
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(validators=[
        MinLengthValidator(7, message="Password must be at least 8 characters"),
        MaxLengthValidator(20, message="Password cannot be more than 20 numbers")
    ],
    write_only=True,
    style={'input_type': 'password'})
    email = serializers.EmailField(validators=[EmailValidator(message="Invalid Email address")])
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