from django.urls import path

from city.views import CityView


urlpatterns = [
    path('all/', CityView.as_view(), name="city"),


]
