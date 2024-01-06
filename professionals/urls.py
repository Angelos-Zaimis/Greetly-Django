from django.urls import path
from professionals.views import ProfessionalListView

urlpatterns = [
    path('', ProfessionalListView.as_view(), name='professional-list'),
]
