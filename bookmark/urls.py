from django.urls import path
from .views import BookMarkList, BookMarkRetrieveDestroyView

urlpatterns = [
    path('', BookMarkList.as_view(), name='bookmark-list'),
    path('<str:uniqueTitle>/', BookMarkRetrieveDestroyView.as_view(), name='get_bookmark_by_title')
]
