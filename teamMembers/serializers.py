from rest_framework import serializers
from teamMembers.models import TeamMembers



class TeamMemberSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembers
        fields = ['id','email', 'location', 'name', 'occupation','languageOne','languageTwo','languageThree','languageFour', 'profileImage']




