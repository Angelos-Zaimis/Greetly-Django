from django.urls import path
from django.urls import path
from .views import upload_and_translate

urlpatterns = [
    path('', upload_and_translate, name='upload_and_translate'),
]