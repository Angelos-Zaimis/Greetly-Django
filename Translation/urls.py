from django.urls import path
from Translation.views import TranslateImageView,GetImagesView


urlpatterns = [
    path('getImage', GetImagesView.as_view(), name="GetImage"),
    path('', TranslateImageView.as_view(), name='translate-TranslateImage'),
]
