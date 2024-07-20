# standard imports.
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# third part imports.
from rest_framework_simplejwt.authentication import JWTAuthentication

# local imports
from .serializers import UserSerializer, StaffMemberSerializer
from exceptions.restapi import CustomAPIException
from apps.accounts.services import *
from apps.accounts.services import create_user, update_user


class RegisterAPI(APIView):
    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField( max_length=20 )
        last_name = serializers.CharField( max_length=20, required=False )
        image = serializers.ImageField( required=False )
        email = serializers.EmailField( required=True )
        password = serializers.CharField( required=True )
        role = serializers.ChoiceField( choices=USER_ROLES, default="staff" )

    def post(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
   
        user = create_user( **serializer.validated_data )
        return Response({"data": UserSerializer(user, context={"request":request}).data})
        
    def patch(self, request, *args,  **kwargs):
        # need to work
        user = update_user(**request.data)
        return Response({"data": UserSerializer(user, context={"request":request}).data})


class UserProfileAPI(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request":request})
        response = {
            "status":200,
            "data":serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK)
    

class AddNewStaffMemberAPI(APIView):
    authentication_classes = [JWTAuthentication]

    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField( max_length=20 )
        last_name = serializers.CharField( max_length=20, required=False )
        image = serializers.ImageField( required=False )
        email = serializers.EmailField( required=True )
        password = serializers.CharField( required=True )
    
    def post(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user = create_staff_member(manager=request.user, **serializer.validated_data)
        return Response({"data": StaffMemberSerializer(user, context={"request":request}).data})
    

class GetStaffMembersDetailAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args,  **kwargs):
        staff_members = get_all_staff_members(manager=request.user)
        output_serializer = StaffMemberSerializer(staff_members, many=True)
        return Response({"data": output_serializer.data })


class UpdateStaffMemberDetailsAPI(APIView):
    authentication_classes = [JWTAuthentication]

    class InputSerializer(serializers.Serializer):
        employee_id = serializers.CharField( max_length=20 )
        first_name = serializers.CharField( max_length=20 )
        last_name = serializers.CharField( max_length=20, required=False )
        image = serializers.ImageField( required=False )
       
    def patch(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user = update_staff_member_details(manager=request.user, **serializer.validated_data)
        return Response({"data": StaffMemberSerializer(user, context={"request":request}).data})
  