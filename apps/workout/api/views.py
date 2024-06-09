from rest_framework.views import APIView
from rest_framework import serializers
from exceptions.restapi import CustomAPIException
from apps.gym.services import *
from rest_framework.response import Response
from authentication.firebase import FirebaseAuthentication
from apps.gym.api.serializers import UserFitnessCentreSerializer, FitnessCentreMembershipSerializer, MembershipSerializer
from apps.gym.models import FitnessCentre, FitnessCentreMembership
from rest_framework import status
from apps.workout.services import *
from .serializers import *

class GetBodyPartsAPI(APIView):
    def get(self, request):
        upper_body_parts = get_all_body_parts(body_part_type="upper")
        lower_body_parts = get_all_body_parts(body_part_type="lower")

        upper_body_part_serializer = BodyPartSerializer(upper_body_parts, many=True)
        lower_body_part_serializer = BodyPartSerializer(lower_body_parts, many=True)

        return Response({"data": {
            "upper": upper_body_part_serializer.data,
            "lower": lower_body_part_serializer.data
        }})
    
class GetBodyPartExcercisesAPI(APIView):
    class InputSerializer(serializers.Serializer):
        body_part_id = serializers.IntegerField()

    def get(self, request, **kwargs):
        serializer = self.InputSerializer(data=self.kwargs)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        body_parts = get_body_part_excercises(**serializer.data)

        serializer = ExerciseSerializer(body_parts, many=True)

        return Response({"data": serializer.data})