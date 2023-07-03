from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from teamMembers.serializers import TeamMemberSerialiazer
from .models import TeamMembers
from rest_framework import generics



class TeamMemberListView(generics.ListAPIView):
    queryset = TeamMembers.objects.all()
    serializer_class = TeamMemberSerialiazer



class TeamMemberView(RetrieveAPIView):
    queryset = TeamMembers.objects.all()
    serializer_class = TeamMemberSerialiazer
