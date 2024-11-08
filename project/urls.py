
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from custom_user.views import UserProvider
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
    # GET CITY , CATEGORY,INFORMATION
    path('middleware-info/cities/', include('Cities.urls')),

    # LANGUAGE
    path('middleware-info/userInfo/', UserProvider.as_view(), name='get_userinfo'),

    # TEAM MEMBERS
    path('middleware-info/professionals/', include('professionals.urls')),

    # BOOKMARKS
    path('middleware-info/bookmarks/', include('bookmark.urls')),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)