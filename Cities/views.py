from rest_framework import status, generics, viewsets
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from Cities.models import City, Information,Category
from .serializers import CitySerializer, InformationSerializer ,CategorySerializer



class GetCitiesView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer




class InformationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InformationSerializer

    def retrieve(self, request, city=None, category=None, information=None):
        queryset = Information.objects.filter(
            category__city__name=city,
            category__name=category,
            title=information
        )
        information_instance = get_object_or_404(queryset)

        serializer = self.get_serializer(information_instance)
        return Response(serializer.data)


class CityCategoriesAPIView(APIView):
    def get(self, request, city):
        try:
            city_obj = City.objects.get(name=city)
            categories = Category.objects.filter(city=city_obj)
            category_names = [category.name for category in categories]
            return Response(category_names)
        except City.DoesNotExist:
            return Response("City not found", status=404)


class CityCategoryInformationAPIView(APIView):
    def get(self, request, city, category):
        try:
            city_obj = City.objects.get(name=city)
            category_obj = Category.objects.get(name=category, city=city_obj)
            # Assuming you have an 'Information' model related to categories
            information = Information.objects.filter(category=category_obj)
            # Serialize the information data if needed
            serialized_information = InformationSerializer(information, many=True).data
            return Response(serialized_information)
        except (City.DoesNotExist, Category.DoesNotExist):
            return Response("City or Category not found", status=404)
