from django.urls import path
from Cities.views import GetCitiesView,InformationViewSet,CityCategoriesAPIView,CityCategorySubCategoriesAPIView,InformationView,GetCitiesBasedOnCategory

urlpatterns = [
    path('', GetCitiesView.as_view()),
    path('region/', GetCitiesBasedOnCategory.as_view(), name="cities_basedon_region"),
    path('<str:city>/categories/', CityCategoriesAPIView.as_view(), name='city_categories'),
    path('<str:city>/<str:category>/subcategories/', CityCategorySubCategoriesAPIView.as_view(), name='category_information'),
    path('<str:city>/<str:category>/<str:subcategory>/', InformationViewSet.as_view({'get': 'retrieve'}),name='subcategory'),
    path('<str:city>/<str:category>/<str:subcategory>/<str:information>/', InformationView.as_view(), name='inforamtion')
]
