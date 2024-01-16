from rest_framework import status
from rest_framework.generics import get_object_or_404, ListAPIView
from urllib.parse import urljoin
from .serializers import CitySerializer, SubCategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import City, Category, SubCategory, Information
from .serializers import InformationSerializer
from django.contrib.sites.shortcuts import get_current_site
from urllib.parse import unquote
from rest_framework.permissions import IsAuthenticated


class GetCitiesView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


# FETCHES CITIES BASED ON REGION(FOR FUTURE IMPLEMENTATION)
class GetCitiesBasedOnCategory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        canton_region = request.query_params.get('region')
        if not canton_region:
            return Response({"message": "The 'region' query parameter cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = City.objects.filter(canton_region=canton_region)
        if queryset.exists():
            serializer = CitySerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({"message": "No cities found in that region"}, status=status.HTTP_404_NOT_FOUND)
# FETCHING CATEGORIES OF CITY
class CityCategoriesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, city):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            city_obj = City.objects.get(name=city)
            categories = Category.objects.filter(city=city_obj)
            category_data = []
            for category in categories:
                image_url = None
                image_tablet_url = None  # Initialize icon_url with a default value
                if category.image:
                    current_site = get_current_site(request)
                    protocol = 'https' if request.is_secure() else 'http'
                    image_url = urljoin(f"{protocol}://{current_site}", category.image.url)

                if category.table_image:
                    current_site = get_current_site(request)
                    protocol = 'https' if request.is_secure() else 'http'
                    image_tablet_url = urljoin(f"{protocol}://{current_site}", category.table_image.url)
                category_data.append({
                    'name': category.name,
                    'icon': category.icon,
                    'description': category.description
                })

                response = {
                    'categories': category_data,
                    'image_url': image_url,
                    'tablet_image': image_tablet_url
                }
            return Response(response)
        except City.DoesNotExist:
            return Response({"message": "City not found"}, status=status.HTTP_404_NOT_FOUND)


# FETCHES THE SUBCATEGORY OF A CATEGORY
class CityCategorySubCategoriesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, city, category):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            city_obj = City.objects.get(name=city)
            category_obj = Category.objects.get(name=category, city=city_obj)
            subcategories = SubCategory.objects.filter(category=category_obj)

            serialized_subcategories = SubCategorySerializer(subcategories, many=True).data

            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'

            image_url = urljoin(f"{protocol}://{current_site}", serialized_subcategories[0]['image'])
            table_image_url = urljoin(f"{protocol}://{current_site}", serialized_subcategories[0]['table_image'])

            for subcategory in serialized_subcategories:
                subcategory.pop('image', None)  # Remove 'image' if it exists
                subcategory.pop('table_image', None)  # Remove 'table_image' if it exists

            result = {
                'subcategories': serialized_subcategories,
                'image_url': image_url,
                'tablet_image_url': table_image_url
            }
            return Response(result)
        except (City.DoesNotExist, Category.DoesNotExist):
            return Response({"message": "City or Category not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, city, category):
        city_obj = get_object_or_404(City, name=city)
        category_obj = get_object_or_404(Category, name=category, city=city_obj)
        subcategories = SubCategory.objects.filter(category=category_obj)
        serialized_subcategories = SubCategorySerializer(subcategories, many=True).data
        current_site = get_current_site(request)
        protocol = 'https' if request.is_secure() else 'http'

        for subcategory in serialized_subcategories:
            if 'image' in subcategory:
                image_url = f"{protocol}://{current_site}{subcategory['image']}"
                subcategory['image'] = image_url

        return Response(serialized_subcategories)


# GET INFORMATION FOR CATEGORY/SUBCATEGORY
class InformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, city, category, subcategory, information):
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        try:
            city_obj = City.objects.get(name=city)
            category_obj = Category.objects.get(name=category, city=city_obj)
            subcategory_obj = SubCategory.objects.get(title=subcategory, category=category_obj)
            information_obj = Information.objects.get(subcategory=subcategory_obj, title=information)
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            image_url = f"{protocol}://{current_site}{unquote(str(information_obj.image))}"
            information_obj.image = image_url

            serializer = InformationSerializer(information_obj)
            return Response(serializer.data)

        except (City.DoesNotExist, Category.DoesNotExist, SubCategory.DoesNotExist, Information.DoesNotExist):
            return Response({"message": "Information not found."}, status=404)
