from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from urllib.parse import urljoin
from .serializers import CitySerializer, SubCategorySerializer, CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import City, Category, SubCategory, Information
from .serializers import InformationSerializer


class GetCitiesView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class InformationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InformationSerializer

    def retrieve(self, request, city=None, category=None, information=None):
        queryset = Information.objects.filter(
            subcategory__category__city__name=city,
            subcategory__category__name=category,
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
            return Response("City not found", status=404)


from django.contrib.sites.shortcuts import get_current_site


class CityCategorySubCategoriesAPIView(APIView):
    def get(self, request, city, category):
        try:
            city_obj = City.objects.get(name=city)
            category_obj = Category.objects.get(name=category, city=city_obj)
            subcategories = SubCategory.objects.filter(category=category_obj)
            serialized_subcategories = SubCategorySerializer(subcategories, many=True).data

            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'

            for subcategory in serialized_subcategories:
                if 'image' in subcategory:
                    image_url = urljoin(f"{protocol}://{current_site}", subcategory['image'])
                if 'table_image' in subcategory:
                    table_image_url = urljoin(f"{protocol}://{current_site}", subcategory['table_image'])

            # Create a dictionary to hold the result
            result = {
                'subcategories': serialized_subcategories,
                'image_url': image_url,
                'tablet_image_url': table_image_url
            }
            return Response(result)
        except (City.DoesNotExist, Category.DoesNotExist):
            return Response("City or Category not found", status=status.HTTP_404_NOT_FOUND)

    def put(self, request, city, category):
        city_obj = get_object_or_404(City, name=city)
        category_obj = get_object_or_404(Category, name=category, city=city_obj)

        # Process the PUT request to change the category

        # Retrieve the new subcategories for the updated category
        subcategories = SubCategory.objects.filter(category=category_obj)
        serialized_subcategories = SubCategorySerializer(subcategories, many=True).data

        current_site = get_current_site(request)
        protocol = 'https' if request.is_secure() else 'http'

        # Add "http://" or "https://" prefix to image URLs
        for subcategory in serialized_subcategories:
            if 'image' in subcategory:
                image_url = f"{protocol}://{current_site}{subcategory['image']}"
                subcategory['image'] = image_url

        return Response(serialized_subcategories)


from urllib.parse import unquote


class InformationView(APIView):
    def get(self, request, city, category, subcategory, information):
        try:
            city_obj = City.objects.get(name=city)
            category_obj = Category.objects.get(name=category, city=city_obj)
            subcategory_obj = SubCategory.objects.get(title=subcategory, category=category_obj)

            # Filter information based on exact title match
            information_obj = Information.objects.get(subcategory=subcategory_obj, title=information)

            # Get the complete image URL
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            image_url = f"{protocol}://{current_site}{unquote(str(information_obj.image))}"
            information_obj.image = image_url

            serializer = InformationSerializer(information_obj)
            return Response(serializer.data)

        except (City.DoesNotExist, Category.DoesNotExist, SubCategory.DoesNotExist, Information.DoesNotExist):
            return Response({"error": "Information not found."}, status=404)
