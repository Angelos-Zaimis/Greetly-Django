from rest_framework import generics
from .models import City
from .serializers import CitySerializer

class CityCreateAPIView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer




class CityDetailView(generics.RetrieveAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def get_object(self):
        name = self.kwargs['name']
        return self.queryset.filter(name__iexact=name).first()