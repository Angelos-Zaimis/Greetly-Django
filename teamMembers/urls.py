from django.urls import path
from teamMembers.views import TeamMemberView, TeamMemberListView

urlpatterns = [
    # ... other URL patterns
    path('', TeamMemberListView.as_view(), name='user_list'),
    path('<int:pk>', TeamMemberView.as_view(), name='user_detail'),
]
