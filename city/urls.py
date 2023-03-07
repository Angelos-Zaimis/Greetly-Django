from django.urls import path

from city.views import CityCreateAPIView


urlpatterns = [
    path('', CityCreateAPIView.as_view()),


]
