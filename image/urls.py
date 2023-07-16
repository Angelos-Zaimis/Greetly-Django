from django.urls import path
from image.views import TranslateImageView

urlpatterns = [
    path('', TranslateImageView.as_view(), name='translate-image'),
]
