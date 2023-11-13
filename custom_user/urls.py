from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from custom_user.views import CustomTokenObtainPairView,ChangePasswordView,ChangePasswordVerify,UserGoogleExists


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('token/verify/', jwt_views.TokenVerifyView.as_view(),
         name='token_refresh'),
    path('changePassword/', ChangePasswordView.as_view(), name='change-password'),
    path('changePasswordVerify/', ChangePasswordVerify.as_view(), name='change-password-verify'),
    path('userExists', UserGoogleExists.as_view(), name='user-exists')
]
