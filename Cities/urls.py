from django.urls import path
from Cities.views import GetCitiesView,InformationViewSet,CityCategoriesAPIView,CityCategoryInformationAPIView

urlpatterns = [
    path('', GetCitiesView.as_view()),
    path('<str:city>/categories', CityCategoriesAPIView.as_view(), name='city_categories'),
    path('<str:city>/<str:category>/informations', CityCategoryInformationAPIView.as_view(), name='category_information'),
    path('<str:city>/<str:category>/<str:information>/', InformationViewSet.as_view({'get': 'retrieve'}),name='information-detail'),
]
