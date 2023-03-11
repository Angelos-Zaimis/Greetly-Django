from django.urls import path

from city.views import CityCreateAPIView, CityDetailView


urlpatterns = [
    path('', CityCreateAPIView.as_view(),name='city-list'),
    path('<str:name>/', CityDetailView.as_view(), name='city-detail'),

]
