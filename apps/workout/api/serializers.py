from rest_framework import serializers
from apps.workout.models import BodyPart, Exercise

class BodyPartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    image = serializers.SerializerMethodField()
    body_part_type = serializers.CharField()

    def get_image(self, obj):
        try:
            request = self.context["request"]
            return request.build_absolute_uri(obj.image.url)
        
        except Exception as e:
            print(e)
            return None


class ExerciseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        try:
            request = self.context["request"]
            return request.build_absolute_uri(obj.image.url)
        
        except Exception as e:
            print(e)
            return None
    