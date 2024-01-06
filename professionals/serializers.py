from rest_framework import serializers
from .models import Professionals


class ProfessionalSerializer(serializers.ModelSerializer):
    occupation = serializers.SerializerMethodField()
    licensed = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    specialization = serializers.SerializerMethodField()
    aboutMe = serializers.SerializerMethodField()

    class Meta:
        model = Professionals
        fields = [
            'email', 'name', 'profileImage', 'languages', 'review', 'type',
            'occupation', 'licensed', 'location', 'specialization', 'aboutMe',
            'latitude', 'longitude', 'latitudeDelta', 'longitudeDelta', 'linkAddress'
        ]

    def get_occupation(self, obj):
        if hasattr(obj, 'insuranceagent'):
            return obj.insuranceagent.occupation
        elif hasattr(obj, 'immigrationconsultant'):
            return obj.immigrationconsultant.occupation
        return None

    def get_licensed(self, obj):
        if hasattr(obj, 'insuranceagent'):
            return obj.insuranceagent.licensed
        elif hasattr(obj, 'immigrationconsultant'):
            return obj.immigrationconsultant.licensed
        return None

    def get_location(self, obj):
        if hasattr(obj, 'insuranceagent'):
            return obj.insuranceagent.location
        elif hasattr(obj, 'immigrationconsultant'):
            return obj.immigrationconsultant.location
        return None

    def get_specialization(self, obj):
        if hasattr(obj, 'insuranceagent'):
            return obj.insuranceagent.specialization
        elif hasattr(obj, 'immigrationconsultant'):
            return obj.immigrationconsultant.specialization
        return None

    def get_aboutMe(self, obj):
        if hasattr(obj, 'insuranceagent'):
            return obj.insuranceagent.aboutMe
        elif hasattr(obj, 'immigrationconsultant'):
            return obj.immigrationconsultant.aboutMe
        return None
