from rest_framework import serializers
from apps.gym.models import FitnessCentre, FitnessCentreMembership

class FitnessCentreMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessCentreMembership
        fields = "__all__"

class FitnessCentreSerializer(serializers.ModelSerializer):
    memberships = FitnessCentreMembershipSerializer(many=True)

    class Meta:
        model = FitnessCentre
        fields = [ "owner", 
                  "name", 
                  "cover_image",
                  "address", 
                  "phone_number", 
                  "description",
                  "memberships"
                  ]
    
    



