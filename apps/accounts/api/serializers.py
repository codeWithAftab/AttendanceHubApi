from rest_framework import serializers
from apps.gym.api.serializers import UserFitnessCentreSerializer, AdminFitnessCentreSerializer

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    image = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    date_of_birth = serializers.DateField()
    zip_code = serializers.IntegerField()
    joined_fitness_centre = UserFitnessCentreSerializer()
    is_partner = serializers.BooleanField()
    address_line = serializers.CharField()
    admin_of_fitness_centre = AdminFitnessCentreSerializer()
    weight = serializers.FloatField()
    height = serializers.FloatField()

    def get_cover_image(self, obj):
        try:
            request = self.context["request"]
            return request.build_absolute_uri(obj.image.url)
        
        except Exception as e:
            print(e)
            return None

    def get_image(self, obj):
        try:
            request = self.context["request"]
            return request.build_absolute_uri(obj.image.url)
        
        except:
            return None
