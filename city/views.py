from rest_framework import generics
from .models import City
from .serializers import CitySerializer

class CityCreateAPIView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
