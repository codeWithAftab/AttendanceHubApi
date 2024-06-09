from rest_framework import serializers
from apps.gym.models import FitnessCentre, FitnessCentreMembership

class FitnessCentreMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessCentreMembership
        fields = "__all__"


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    uuid = serializers.UUIDField()

class UserFitnessCentreSerializer(serializers.Serializer):
    owner = UserSerializer()
    name = serializers.CharField()
    cover_image = serializers.CharField()
    description = serializers.CharField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    memberships = FitnessCentreMembershipSerializer(many=True)

class AdminFitnessCentreSerializer(serializers.Serializer):
    name = serializers.CharField()
    cover_image = serializers.CharField()
    description = serializers.CharField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    memberships = FitnessCentreMembershipSerializer(many=True)


    
class MembershipSerializer(serializers.Serializer):
    member = serializers.CharField()
    # fitness_centre = FitnessCentreSerializer()
    membership_type = FitnessCentreMembershipSerializer()
    start_date = serializers.DateField()
    end_date = serializers.DateField()




