from rest_framework.views import APIView
from rest_framework import serializers
from exceptions.restapi import CustomAPIException
from apps.gym.services import *
from rest_framework.response import Response
from authentication.firebase import FirebaseAuthentication
from apps.gym.api.serializers import FitnessCentreSerializer, FitnessCentreMembershipSerializer
from apps.gym.models import FitnessCentre, FitnessCentreMembership
from rest_framework import status


class RegisterFitnessCentreAPI(APIView):
    authentication_classes = [FirebaseAuthentication]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        description = serializers.CharField()
        phone_number = serializers.CharField()
        zip_code = serializers.CharField()
        address = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        fitness_centre = register_fitness_centre(owner=request.user,
                                                **serializer.data  )
        
        output_serializer = FitnessCentreSerializer(fitness_centre)
        return Response({"data": output_serializer.data}, status=status.HTTP_201_CREATED)


class GetOwnerFitnessCentreAPI(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        fitness_centre = get_fitness_centre_by_owner(owner=request.user)                                
        output_serializer = FitnessCentreSerializer(fitness_centre)
        return Response({"data": output_serializer.data})

class CreateMembershipPlan(APIView):
    authentication_classes = [FirebaseAuthentication]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        membership_type = serializers.CharField()
        price = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        membership = create_membership_plan( owner=request.user, **serializer.data)
        output_serializer = FitnessCentreMembershipSerializer(membership)
        
        return Response({"data": output_serializer.data})
    
class DeleteMembershipPlan(APIView):
    authentication_classes = [FirebaseAuthentication]

    class InputSerializer(serializers.Serializer):
        membership_id = serializers.IntegerField()

    def delete(self, request, **kwargs):
        serializer = self.InputSerializer(data=self.kwargs)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        delete_membership_plan( owner=request.user, **serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UpdateMembershipPlan(APIView):
    authentication_classes = [FirebaseAuthentication]

    class InputSerializer(serializers.Serializer):
        membership_id = serializers.IntegerField()
        title = serializers.CharField(required=False)
        membership_type = serializers.CharField(required=False)
        price = serializers.CharField(required=False)

    def patch(self, request, **kwargs):
        request_data = request.data.copy()
        request_data.update(self.kwargs)
        serializer = self.InputSerializer(data=request_data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        membership = update_membership_plan( owner=request.user, **serializer.data)
        output_serializer = FitnessCentreMembershipSerializer(membership)
        
        return Response({"data": output_serializer.data})

class GetOwnerFitnessCentreAPI(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        fitness_centre = get_fitness_centre_by_owner(owner=request.user)                                
        output_serializer = FitnessCentreSerializer(fitness_centre)
        return Response({"data": output_serializer.data})


class AddMemberToFitnessCentreAPI(APIView):
    authentication_classes = [FirebaseAuthentication]
    
    class InputSerializer(serializers.Serializer):
        user_id = serializers.UUIDField()
       
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user_id = serializer.data["user_id"]
        fitness_centre = add_user_to_fitness_centre( owner=request.user, 
                                                     user_id=user_id )
        output_serializer = FitnessCentreSerializer(fitness_centre)
        return Response({"data": output_serializer.data})

class RemoveMemberFromFitnessCentreAPI(APIView):
    authentication_classes = [FirebaseAuthentication]
    
    class InputSerializer(serializers.Serializer):
        user_id = serializers.UUIDField()
       
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user_id = serializer.data["user_id"]
        fitness_centre = add_user_to_fitness_centre( owner=request.user, 
                                                     user_id=user_id )
        output_serializer = FitnessCentreSerializer(fitness_centre)
        return Response({"data": output_serializer.data})
        
        

