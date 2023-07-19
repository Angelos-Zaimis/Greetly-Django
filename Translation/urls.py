from django.urls import path
from Translation.views import TranslateImageView


urlpatterns = [
    path('', TranslateImageView.as_view(), name='translate-TranslateImage'),
]
