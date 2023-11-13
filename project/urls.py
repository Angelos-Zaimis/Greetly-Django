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
        title="middleware-information",
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
    path('middleware-info/auth/', include('custom_user.urls')),

    # REGISTRATION
    path('middleware-info/auth/', include('registration.urls')),

    # SWAGGER PATHS
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),
    # GET CITY , CATEGORY,INFORMATION
    path('middleware-info/cities/', include('Cities.urls')),

    path('middleware-info/translateImage/', include('Translation.urls')),

    # LANGUAGE
    path('middleware-info/userInfo/', UserProvider.as_view(), name='get_userinfo'),

    # TEAM MEMBERS
    path('middleware-info/teamMembers/', include('teamMembers.urls')),

    # BOOKMARKS
    path('middleware-info/bookmarks/', include('bookmark.urls')),

    # payments
    path('middleware-info/payments/', include('payments.urls'))


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)