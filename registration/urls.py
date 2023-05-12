from django.urls import path

from .views import RegistrationView,VerifyRegistrationView


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name="register"),
    path('register/verify/', VerifyRegistrationView.as_view(), name="verify_registration"),
]
