from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from custom_user.views import ChangePasswordView, ChangePasswordVerify, UserGoogleExists, GoogleLoginView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='token_obtain_pair'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('changePassword/', ChangePasswordView.as_view(), name='change-password'),

    path('changePasswordVerify/', ChangePasswordVerify.as_view(), name='change-password-verify'),

    path('userExists', UserGoogleExists.as_view(), name='user-exists'),

    path('google-login/', GoogleLoginView.as_view(), name='google_login'),
]
