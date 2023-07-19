"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views
from custom_user.views import CustomTokenObtainPairView,UserProvider
from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="middleware-informations",
        default_version='v1',
        description="Backend-API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # ADMIN PANEL
    path('admin/', admin.site.urls),

    # GET TOKEN / LOGIN
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/auth/token/verify/', jwt_views.TokenVerifyView.as_view(),
         name='token_refresh'),

    # REGISTRATION
    path('api/auth/', include('registration.urls')),

    # SWAGGER PATHS
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
    # GET CITY , CATEGORY,INFORMATION
    path('api/cities/', include('Cities.urls')),

    path('api/translateImage/', include('Translation.urls')),

    # LANGUAGE
    path('api/userInfo/', UserProvider.as_view(), name='get_userinfo'),

    # TEAM MEMBERS
    path('api/teamMembers/', include('teamMembers.urls')),

    # BOOKMARKS
    path('api/bookmarks/', include('bookmark.urls'))


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)