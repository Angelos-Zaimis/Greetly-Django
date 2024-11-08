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

class GetCitiesBasedOnCategory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Get cities based on the provided region."""
        if not request.user.is_authenticated:
            return self.build_unauthenticated_response()

        canton_region = request.query_params.get('region')
        if not canton_region:
            return self.build_bad_request_response("The 'region' query parameter cannot be empty.")

        queryset = self.get_cities_by_region(canton_region)
        if queryset.exists():
            return self.build_success_response(queryset, request)

        return self.build_not_found_response()

    @staticmethod
    def build_unauthenticated_response():
        """Return response for unauthenticated access."""
        return Response({'detail': 'Authentication credentials were not provided.'},
                        status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def build_bad_request_response(message):
        """Return response for bad requests."""
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_cities_by_region(region):
        """Filter and return cities based on the region."""
        return City.objects.filter(canton_region=region)

    @staticmethod
    def build_success_response(queryset, request):
        """Serialize and return the successful response with city data."""
        serializer = CitySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    def build_not_found_response():
        """Return response when no cities are found."""
        return Response({"message": "No cities found in that region"}, status=status.HTTP_404_NOT_FOUND)


class CityCategoriesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, city):
        """Get categories for a given city."""
        if not request.user.is_authenticated:
            return self.build_unauthenticated_response()

        city_obj = self.get_city_by_name(city)
        if not city_obj:
            return self.build_not_found_response()

        categories = Category.objects.filter(city=city_obj)
        category_data = self.build_category_data(categories, request)

        response = {
            'categories': category_data,
        }

        return Response(response, status=status.HTTP_200_OK)

    # Helper functions
    @staticmethod
    def build_unauthenticated_response():
        """Return response for unauthenticated access."""
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def get_city_by_name(city_name):
        """Retrieve a city by name or return None if not found."""
        try:
            return City.objects.get(name=city_name)
        except City.DoesNotExist:
            return None

    def build_category_data(self, categories, request):
        """Build and return category data with image URLs."""
        category_data = []
        for category in categories:
            category_data.append({
                'name': category.name,
                'icon': category.icon,
                'description': category.description,
                'image_url': self.get_image_url(category.image, request),
                'tablet_image': self.get_image_url(category.table_image, request),
            })
        return category_data

    @staticmethod
    def get_image_url(image_field, request):
        """Generate a full image URL if the image field is present."""
        if image_field:
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            return urljoin(f"{protocol}://{current_site}", image_field.url)
        return None

    @staticmethod
    def build_not_found_response():
        """Return response when a city is not found."""
        return Response({"message": "City not found"}, status=status.HTTP_404_NOT_FOUND)

class CityCategorySubCategoriesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, city, category):
        """Get subcategories for a given city and category."""
        if not request.user.is_authenticated:
            return self.build_unauthenticated_response()

        city_obj, category_obj = self.get_city_and_category(city, category)
        if not city_obj or not category_obj:
            return self.build_not_found_response()

        subcategories = SubCategory.objects.filter(category=category_obj)
        serialized_subcategories = SubCategorySerializer(subcategories, many=True).data

        image_url, table_image_url = self.build_image_urls(serialized_subcategories, request)
        self.remove_image_fields(serialized_subcategories)

        result = {
            'subcategories': serialized_subcategories,
            'image_url': image_url,
            'tablet_image_url': table_image_url
        }
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, city, category):
        """Update subcategories for a given city and category."""
        city_obj = get_object_or_404(City, name=city)
        category_obj = get_object_or_404(Category, name=category, city=city_obj)
        subcategories = SubCategory.objects.filter(category=category_obj)
        serialized_subcategories = SubCategorySerializer(subcategories, many=True).data

        self.add_image_urls_to_subcategories(serialized_subcategories, request)

        return Response(serialized_subcategories, status=status.HTTP_200_OK)

    # Helper functions
    @staticmethod
    def build_unauthenticated_response():
        """Return response for unauthenticated access."""
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def build_not_found_response():
        """Return response when a city or category is not found."""
        return Response({"message": "City or Category not found"}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_city_and_category(city_name, category_name):
        """Retrieve the city and category objects or return None if not found."""
        try:
            city_obj = City.objects.get(name=city_name)
            category_obj = Category.objects.get(name=category_name, city=city_obj)
            return city_obj, category_obj
        except (City.DoesNotExist, Category.DoesNotExist):
            return None, None

    @staticmethod
    def build_image_urls(subcategories, request):
        """Build and return image URLs for subcategories."""
        if subcategories:
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            image_url = urljoin(f"{protocol}://{current_site}", subcategories[0].get('image', ''))
            table_image_url = urljoin(f"{protocol}://{current_site}", subcategories[0].get('table_image', ''))
            return image_url, table_image_url
        return None, None

    @staticmethod
    def remove_image_fields(subcategories):
        """Remove 'image' and 'table_image' fields from subcategory data."""
        for subcategory in subcategories:
            subcategory.pop('image', None)
            subcategory.pop('table_image', None)

    @staticmethod
    def add_image_urls_to_subcategories(subcategories, request):
        """Add full image URLs to subcategories."""
        current_site = get_current_site(request)
        protocol = 'https' if request.is_secure() else 'http'
        for subcategory in subcategories:
            if 'image' in subcategory:
                image_url = f"{protocol}://{current_site}{subcategory['image']}"
                subcategory['image'] = image_url

class InformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, city, category, subcategory, information):
        """Retrieve detailed information for a given city, category, subcategory, and information title."""
        if not request.user.is_authenticated:
            return self.build_unauthenticated_response()

        city_obj, category_obj, subcategory_obj, information_obj = self.get_objects(city, category, subcategory, information)
        if not all([city_obj, category_obj, subcategory_obj, information_obj]):
            return self.build_not_found_response()

        self.set_image_url(information_obj, request)
        serializer = InformationSerializer(information_obj)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Helper functions
    @staticmethod
    def build_unauthenticated_response():
        """Return response for unauthenticated access."""
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def build_not_found_response():
        """Return response when city, category, subcategory, or information is not found."""
        return Response({"message": "Information not found."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def get_objects(city, category, subcategory, information):
        """Retrieve city, category, subcategory, and information objects."""
        try:
            city_obj = City.objects.get(name=city)
            category_obj = Category.objects.get(name=category, city=city_obj)
            subcategory_obj = SubCategory.objects.get(title=subcategory, category=category_obj)
            information_obj = Information.objects.get(subcategory=subcategory_obj, title=information)
            return city_obj, category_obj, subcategory_obj, information_obj
        except (City.DoesNotExist, Category.DoesNotExist, SubCategory.DoesNotExist, Information.DoesNotExist):
            return None, None, None, None

    @staticmethod
    def set_image_url(information_obj, request):
        """Set the full image URL for the information object."""
        current_site = get_current_site(request)
        protocol = 'https' if request.is_secure() else 'http'
        information_obj.image = f"{protocol}://{current_site}{unquote(str(information_obj.image))}"
